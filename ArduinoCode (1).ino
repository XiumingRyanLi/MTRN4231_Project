// === Gripper firmware for Arduino Nano (ATmega328P) ===
// Works with both positional and continuous-rotation servos.
// Toggle SERVO_CONTINUOUS below as needed.

// Protocol (newline-terminated commands):
//   CMD OPEN
//   CMD CLOSE
//   CMD STOP
//   QRY STATE
//   EFFORT <float>              // accepted, stored, not enforced
//   SET CLOSE_MAX <int>         // 0..120 (safety clamp), used in both modes
//   CMD CLOSE ANGLE <int>       // explicit target (positional: degrees; continuous: time-proportional)
// Responses: ACK ... / STATE open=...,force=...

#include <Servo.h>

// ======= CONFIG =======
constexpr bool SERVO_CONTINUOUS = false;   // <-- set true if your servo spins endlessly on write()
constexpr int SERVO_PIN        = 9;
constexpr int OPEN_ANGLE       = 0;
constexpr int DEFAULT_CLOSEMAX = 120;
constexpr int HARD_MAX_CLOSE   = 120;
constexpr int MIN_US           = 1000;    // safer bounds for many hobby servos
constexpr int MAX_US           = 2000;

// Positional mode motion profile
constexpr int STEP_SIZE_DEG    = 2;
constexpr unsigned long STEP_PERIOD_MS   = 10;
constexpr unsigned long STATE_PERIOD_MS  = 200;
constexpr int OPEN_THRESH_DEG  = 3;

// Continuous-rotation mode timings/speeds
constexpr int CR_NEUTRAL_US    = 1500;    // stop
constexpr int CR_OPEN_US       = 1300;    // tweak if needed (lower than neutral → one direction)
constexpr int CR_CLOSE_US      = 1700;    // higher than neutral → opposite direction
constexpr unsigned long CR_OPEN_MS_DEFAULT  = 700;   // how long to run for a "full" OPEN
constexpr unsigned long CR_CLOSE_MS_DEFAULT = 700;   // how long to run for a "full" CLOSE

Servo gate;

// Shared state
volatile bool moving            = false;
float last_effort_N             = 0.0f;
unsigned long last_state_ms     = 0;
int close_max_deg               = DEFAULT_CLOSEMAX;

// Positional mode state
int current_deg                 = OPEN_ANGLE;
int target_deg                  = OPEN_ANGLE;
unsigned long last_step_ms      = 0;

// Continuous mode state
enum class CrDir : uint8_t { Idle, Opening, Closing } cr_dir = CrDir::Idle;
unsigned long cr_stop_deadline_ms = 0;
unsigned long cr_open_ms  = CR_OPEN_MS_DEFAULT;
unsigned long cr_close_ms = CR_CLOSE_MS_DEFAULT;

// --- helpers ---
static inline int clampInt(int v, int lo, int hi) {
  if (v < lo) return lo;
  if (v > hi) return hi;
  return v;
}

void writeServoDeg(int deg) { // positional
  deg = clampInt(deg, 0, 180);
  gate.write(deg);
  current_deg = deg;
}

void writeServoUs(int us) { // continuous / attach bounds respected by Servo lib anyway
  gate.writeMicroseconds(us);
}

bool isOpenBit() {
  if (SERVO_CONTINUOUS) {
    // Heuristic: "open" = last commanded was OPEN and we are not moving now
    return (cr_dir == CrDir::Idle);  // no true position feedback available
  } else {
    return (abs(current_deg - OPEN_ANGLE) <= OPEN_THRESH_DEG);
  }
}

void emitState() {
  Serial.print(F("STATE open="));
  Serial.print(isOpenBit() ? 1 : 0);
  Serial.print(F(",force="));
  Serial.println(last_effort_N, 2);
}

void ack(const char* msg) {
  Serial.print(F("ACK "));
  Serial.println(msg);
}

// ======= Motion control =======

void stopMotion() {
  moving = false;
  if (SERVO_CONTINUOUS) {
    cr_dir = CrDir::Idle;
    cr_stop_deadline_ms = 0;
    writeServoUs(CR_NEUTRAL_US); // hard stop
  }
  ack("STOP");
  emitState();
}

// Positional start
void startMoveToPositional(int deg) {
  target_deg = clampInt(deg, 0, close_max_deg);
  moving = (target_deg != current_deg);
  ack(moving ? "EXEC" : "NOOP");
  last_step_ms = 0; // step asap
}

// Continuous "movement" as a timed run
void startMoveContinuous(CrDir dir, unsigned long run_ms) {
  if (run_ms == 0) {
    // No motion requested
    cr_dir = CrDir::Idle;
    writeServoUs(CR_NEUTRAL_US);
    moving = false;
    ack("NOOP");
    return;
  }
  cr_dir = dir;
  moving = true;
  const unsigned long now = millis();
  cr_stop_deadline_ms = now + run_ms;
  if (dir == CrDir::Opening) {
    writeServoUs(CR_OPEN_US);
    ack("OPEN");
  } else if (dir == CrDir::Closing) {
    writeServoUs(CR_CLOSE_US);
    ack("CLOSE");
  } else {
    writeServoUs(CR_NEUTRAL_US);
    ack("NOOP");
    moving = false;
  }
}

void handleMotionPositional() {
  if (!moving) return;
  const unsigned long now = millis();
  if (now - last_step_ms < STEP_PERIOD_MS) return;
  last_step_ms = now;

  int diff = target_deg - current_deg;
  if (diff == 0) {
    moving = false;
    emitState();
    return;
  }
  int step = (diff > 0) ? STEP_SIZE_DEG : -STEP_SIZE_DEG;
  if (abs(diff) < abs(step)) step = diff;
  writeServoDeg(current_deg + step);
}

void handleMotionContinuous() {
  if (!moving) return;
  const unsigned long now = millis();
  if (cr_stop_deadline_ms != 0 && now >= cr_stop_deadline_ms) {
    // auto-stop at deadline
    writeServoUs(CR_NEUTRAL_US);
    cr_dir = CrDir::Idle;
    moving = false;
    emitState();
  }
}

void maybeEmitState() {
  const unsigned long now = millis();
  if (now - last_state_ms >= STATE_PERIOD_MS) {
    last_state_ms = now;
    emitState();
  }
}

// Map "angle" request to time for continuous mode
unsigned long angleToRunMs(int requested_deg) {
  requested_deg = clampInt(requested_deg, 0, close_max_deg);
  const float frac = (close_max_deg > 0) ? (float)requested_deg / (float)close_max_deg : 0.0f;
  // choose the longer of open/close for scaling to avoid under-running
  const unsigned long full_ms = (cr_close_ms > cr_open_ms) ? cr_close_ms : cr_open_ms;
  return (unsigned long)(frac * (float)full_ms);
}

// ======= Command parsing =======
void handleLine(String line) {
  line.trim();
  if (line.length() == 0) return;

  // Don't upcase numbers; but commands are safe to upper
  String u = line;
  u.toUpperCase();

  if (u.startsWith(F("EFFORT "))) {
    String v = line.substring(7);         // from original (preserve case for numeric)
    last_effort_N = v.toFloat();
    ack("EFFORT");
    return;
  }

  if (u.startsWith(F("SET CLOSE_MAX "))) {
    String v = line.substring(String("SET CLOSE_MAX ").length());
    int deg = v.toInt();
    deg = clampInt(deg, 0, HARD_MAX_CLOSE);
    close_max_deg = deg;
    Serial.print(F("ACK SET CLOSE_MAX "));
    Serial.println(close_max_deg);
    return;
  }

  if (u.startsWith(F("CMD CLOSE ANGLE "))) {
    String v = line.substring(String("CMD CLOSE ANGLE ").length());
    int deg = clampInt(v.toInt(), 0, HARD_MAX_CLOSE);
    deg = clampInt(deg, 0, close_max_deg);
    if (SERVO_CONTINUOUS) {
      // run proportionally, then auto-stop
      unsigned long ms = angleToRunMs(deg);
      startMoveContinuous(CrDir::Closing, ms);
    } else {
      startMoveToPositional(deg);
      Serial.println(F("ACK CLOSE")); // maintain UX similar to simple CLOSE
    }
    return;
  }

  if (u == F("CMD OPEN")) {
    if (SERVO_CONTINUOUS) {
      startMoveContinuous(CrDir::Opening, cr_open_ms);
    } else {
      startMoveToPositional(OPEN_ANGLE);
      ack("OPEN");
    }
    return;
  }

  if (u == F("CMD CLOSE")) {
    if (SERVO_CONTINUOUS) {
      startMoveContinuous(CrDir::Closing, cr_close_ms);
    } else {
      startMoveToPositional(close_max_deg);
      ack("CLOSE");
    }
    return;
  }

  if (u == F("CMD STOP")) {
    stopMotion();
    return;
  }

  if (u == F("QRY STATE")) {
    ack("STATE");
    emitState();
    return;
  }

  Serial.print(F("ERR UNKNOWN: "));
  Serial.println(line);
}

// ======= Setup/loop =======
void setup() {
  Serial.begin(115200);
  gate.attach(SERVO_PIN, MIN_US, MAX_US);

  if (SERVO_CONTINUOUS) {
    writeServoUs(CR_NEUTRAL_US);   // ensure stopped
  } else {
    writeServoDeg(OPEN_ANGLE);     // start opened
  }
  moving = false;
  close_max_deg = clampInt(DEFAULT_CLOSEMAX, 0, HARD_MAX_CLOSE);

  Serial.println(F("Gripper Nano v2 ready"));
  Serial.print(F("MODE=")); Serial.println(SERVO_CONTINUOUS ? F("CONTINUOUS") : F("POSITIONAL"));
  Serial.print(F("CLOSE_MAX=")); Serial.println(close_max_deg);
  emitState();
}

void loop() {
  // Motion
  if (SERVO_CONTINUOUS) {
    handleMotionContinuous();
  } else {
    handleMotionPositional();
  }

  if (moving) {
    maybeEmitState();
  }

  // Read commands
  static String buf;
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\r') continue;
    if (c == '\n') {
      handleLine(buf);
      buf = "";
    } else if (buf.length() < 80) {
      buf += c;
    } else {
      buf = "";
    }
  }
}
