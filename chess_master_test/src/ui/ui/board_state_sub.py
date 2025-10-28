import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class ChessBoardSubscriber(Node):

    def __init__(self):
        super().__init__('chess_board_subscriber')
        self.subscription = self.create_subscription(
            String,
            'board_state',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        board = msg.data
        self.get_logger().info(f'\n{board}')


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = ChessBoardSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
