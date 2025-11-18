#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class ChessMoveDetector(Node):
    def __init__(self):
        super().__init__('chess_move_detector')
        
        # Subscriber to occupancy topic
        self.occupancy_sub = self.create_subscription(
            String,
            '/chess/occupancy',
            self.occupancy_callback,
            10
        )
        
        # Publisher for detected moves
        self.move_pub = self.create_publisher(
            String,
            '/player_move',
            10
        )
        
        # Store previous occupancy state
        self.occupancy_before = None
        self.get_logger().info('Chess Move Detector Node initialized')
    
    def occupancy_callback(self, msg):
        """Callback when new occupancy data is received"""
        try:
            # Parse the incoming occupancy dictionary
            occupancy_after = json.loads(msg.data)
            
            # Convert keys to strings if they aren't already (JSON may parse them as integers)
            occupancy_after = {str(k): v for k, v in occupancy_after.items()}
            
            # If we have a previous state, check if it's different
            if self.occupancy_before is not None:
                # Check if the occupancy has actually changed
                if self.has_occupancy_changed(self.occupancy_before, occupancy_after):
                    move_info = self.detect_move(self.occupancy_before, occupancy_after)
                    
                    # Publish the detected move
                    move_msg = String()
                    move_msg.data = move_info
                    self.move_pub.publish(move_msg)
                    
                    self.get_logger().info(f"Move detected: {move_info}")
                else:
                    self.get_logger().debug("Occupancy unchanged, skipping move detection")
            
            # Update the previous state
            self.occupancy_before = occupancy_after
            
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Failed to parse occupancy data: {e}")
        except KeyError as e:
            self.get_logger().error(f"Key error in occupancy callback: {e}. Keys: {list(occupancy_after.keys())[:5]}")
        except Exception as e:
            self.get_logger().error(f"Error in occupancy callback: {type(e).__name__}: {e}")
    
    def has_occupancy_changed(self, occupancy_before, occupancy_after):
        """Check if the occupancy state has changed between two dictionaries"""
        # Ensure both dictionaries have string keys for comparison
        occupancy_before = {str(k): v for k, v in occupancy_before.items()}
        occupancy_after = {str(k): v for k, v in occupancy_after.items()}
        
        # Check if they have the same keys
        if set(occupancy_before.keys()) != set(occupancy_after.keys()):
            return True
        
        # Check if any values have changed
        for cell_num in occupancy_before.keys():
            if occupancy_before[cell_num] != occupancy_after[cell_num]:
                return True
        
        return False
    
    def detect_move(self, occupancy_dict_before, occupancy_dict_after):
        """Detect moves between two board states"""
        # Ensure both dictionaries have string keys
        occupancy_dict_before = {str(k): v for k, v in occupancy_dict_before.items()}
        occupancy_dict_after = {str(k): v for k, v in occupancy_dict_after.items()}
        
        from_squares = []
        to_squares = []
        
        for cell_num in occupancy_dict_before.keys():
            before = occupancy_dict_before[cell_num]
            after = occupancy_dict_after[cell_num]
            
            if before in ['black', 'white'] and after == 'empty':
                from_squares.append(cell_num)
            elif before == 'empty' and after in ['black', 'white']:
                to_squares.append(cell_num)
            elif before in ['black', 'white'] and after in ['black', 'white'] and before != after:
                to_squares.append(cell_num)
        
        # Normal move (1 from, 1 to)
        if len(from_squares) == 1 and len(to_squares) == 1:
            from_algebraic = self.cell_to_algebraic(int(from_squares[0]))
            to_algebraic = self.cell_to_algebraic(int(to_squares[0]))
            return f"{from_algebraic}{to_algebraic}"
        self.get_logger().info(f"from squares: {from_squares}, to squares: {to_squares}")
        # Castling (2 from, 2 to - king and rook both move)
        if len(from_squares) == 2 and len(to_squares) == 2:
            castle_move = self.detect_castling(from_squares, to_squares, occupancy_dict_after)
            if castle_move:
                return castle_move
        
        # En passant (2 from, 1 to - attacking pawn moves, captured pawn disappears)
        elif len(from_squares) == 2 and len(to_squares) == 1:
            en_passant_move = self.detect_en_passant(from_squares, to_squares, occupancy_dict_before, occupancy_dict_after)
            if en_passant_move:
                return en_passant_move
        
        return 'Unexpected move pattern detected'
    
    def detect_castling(self, from_squares, to_squares, occupancy_after):
        """Detect if the move is castling"""
        # Convert to integers for easier calculation
        from_cells = [int(sq) for sq in from_squares]
        to_cells = [int(sq) for sq in to_squares]
        
        # Sort to get consistent ordering
        from_cells.sort()
        to_cells.sort()
        
        # Check for white kingside castling (e1-g1, h1-f1)
        # Cell 61 = e1, 64 = h1, 63 = g1, 62 = f1
        if set(from_cells) == {60, 64} and set(to_cells) == {61, 62}:
            return "e1c1"  # White kingside
        
        # Check for white queenside castling (e1-c1, a1-d1)
        # Cell 61 = e1, 57 = a1, 59 = c1, 60 = d1
        if set(from_cells) == {57, 60} and set(to_cells) == {58, 59}:
            return "e1g1"  # White queenside
        
        # Check for black kingside castling (e8-g8, h8-f8)
        # Cell 5 = e8, 8 = h8, 7 = g8, 6 = f8
        if set(from_cells) == {4, 8} and set(to_cells) == {5, 6}:
            return "e8c8"  # Black kingside
        
        # Check for black queenside castling (e8-c8, a8-d8)
        # Cell 5 = e8, 1 = a8, 3 = c8, 4 = d8
        if set(from_cells) == {1, 4} and set(to_cells) == {2, 3}:
            return "e8g8"  # Black queenside
        
        return None
    
    def detect_en_passant(self, from_squares, to_squares, occupancy_before, occupancy_after):
        """Detect if the move is en passant"""
        # En passant has 2 pieces leaving (attacking pawn + captured pawn) and 1 arriving (attacking pawn)
        from_cells = [int(sq) for sq in from_squares]
        to_cell = int(to_squares[0])
        
        # Determine which piece moved and which disappeared
        moving_pawn = None
        captured_pawn = None
        
        for from_cell in from_cells:
            # The moving pawn should end up in the to_square
            # Check if this could be the attacking pawn by seeing if it's diagonal to the destination
            from_row = (from_cell - 1) // 8
            from_col = (from_cell - 1) % 8
            to_row = (to_cell - 1) // 8
            to_col = (to_cell - 1) % 8
            
            # Pawn moves diagonally one square in en passant
            if abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1:
                # Check if the piece in the destination is the same color as this from_square
                if occupancy_before[str(from_cell)] == occupancy_after[str(to_cell)]:
                    moving_pawn = from_cell
                    captured_pawn = [c for c in from_cells if c != moving_pawn][0]
                    break
        
        if moving_pawn and captured_pawn:
            # Verify it's en passant: captured pawn should be on same row as moving pawn's start
            captured_row = (captured_pawn - 1) // 8
            moving_row = (moving_pawn - 1) // 8
            
            if captured_row == moving_row:
                from_algebraic = self.cell_to_algebraic(moving_pawn)
                to_algebraic = self.cell_to_algebraic(to_cell)
                return f"{from_algebraic}{to_algebraic}"
        
        return None
    
    def cell_to_algebraic(self, cell_num):
        """Convert cell number (1-64) to algebraic notation (a1-h8)"""
        cell_num -= 1
        row = cell_num // 8
        col = cell_num % 8
        file = chr(ord('h') - col)  # Convert column to letter (a-h)
        rank = str(8 - row)  # Convert row to rank (8-1)
        return f"{file}{rank}"


def main(args=None):
    rclpy.init(args=args)
    node = ChessMoveDetector()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()