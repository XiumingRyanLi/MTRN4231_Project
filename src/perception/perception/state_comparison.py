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
        #self.occupancy_before = {1: 'black', 2: 'empty', 3: 'black', 4: 'black', 5: 'black', 6: 'black', 7: 'black', 8: 'black', 9: 'black', 10: 'black', 11: 'black', 12: 'black', 13: 'black', 14: 'black', 15: 'black', 16: 'black', 17: 'empty', 18: 'empty', 19: 'black', 20: 'empty', 21: 'empty', 22: 'empty', 23: 'empty', 24: 'empty', 25: 'empty', 26: 'empty', 27: 'empty', 28: 'empty', 29: 'empty', 30: 'empty', 31: 'empty', 32: 'empty', 33: 'empty', 34: 'empty', 35: 'empty', 36: 'white', 37: 'empty', 38: 'empty', 39: 'empty', 40: 'empty', 41: 'empty', 42: 'empty', 43: 'empty', 44: 'empty', 45: 'empty', 46: 'empty', 47: 'empty', 48: 'empty', 49: 'white', 50: 'white', 51: 'white', 52: 'empty', 53: 'white', 54: 'white', 55: 'white', 56: 'white', 57: 'white', 58: 'white', 59: 'white', 60: 'white', 61: 'white', 62: 'white', 63: 'white', 64: 'white'}
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
        
        if len(from_squares) == 1 and len(to_squares) == 1:
            is_capture = occupancy_dict_before[to_squares[0]] in ['black', 'white']
            
            # Convert cell numbers to algebraic notation
            from_algebraic = self.cell_to_algebraic(int(from_squares[0]))
            to_algebraic = self.cell_to_algebraic(int(to_squares[0]))
            
            return  f"{from_algebraic}{to_algebraic}"
                # 'from_square': from_squares[0],
                # 'to_square': to_squares[0],
                # 'piece_color': occupancy_dict_after[to_squares[0]],
                # 'is_capture': is_capture,
               
            
        else:
            return 'Unexpected move pattern detected'
                # 'from_squares': from_squares,
                # 'to_squares': to_squares,
                # 'note': 
            
    
    def cell_to_algebraic(self, cell_num):
        """Convert cell number (0-63) to algebraic notation (a1-h8)"""
        cell_num -= 1
        #self.get_logger().info(cell_num)
        row = cell_num // 8
        #self.get_logger().info("row:" + row)
        col = cell_num % 8
        #self.get_logger().info("col:" + col)

        file = chr(ord('h') - col)  # Convert column to letter (a-h)
        #self.get_logger().info("file:" + file)

        rank = str(8 - row)  # Convert row to rank (8-1)
        #self.get_logger().info("rank:" + rank)

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