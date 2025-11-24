#!/bin/bash

TITLES=(
  "Chess Detector"
  "State Comparison"
  "User Interface"
  "Task Coordinator"
  "Chess Master"
  "DriverServer"
  "MoveitServer"
  "Arm Controller"
  "Gripper"
)

while true; do
    remaining=0

    for t in "${TITLES[@]}"; do
        # Get all windows matching the title
        ids=$(wmctrl -l | awk -v pat="$t" '$0 ~ pat {print $1}')
        for wid in $ids; do
            echo "Closing $t ($wid)"
            wmctrl -ic "$wid"
            remaining=$((remaining + 1))
        done
    done

    # Exit loop when no windows remain
    if [ $remaining -eq 0 ]; then
        echo "All target windows closed."
        break
    fi

    # Give the WM time to process closing
    sleep 0.2
done
