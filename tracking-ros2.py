import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class CameraTrackingNode(Node):
    def __init__(self):
        super().__init__('img_processor')

        self.data_pub = self.create_publisher(Pose2D, '/camera/tracking_coords', 25)
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)

        self.bridge = CvBridge()

        self.is_catched = False

    def image_callback(self, msg):
        xcor = 0.0
        ycor = 0.0
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # TODO: 
            # Если обект найден, то self.is_catched = True
            
            cv2.imshow("WSL ROS Topic Viewer", frame)
            cv2.waitKey(1)


            pose_msg = Pose2D()
            pose_msg.x = float(xcor)
            pose_msg.y = float(ycor)
            pose_msg.theta = 1.0 if self.is_catched is True else 0.0


        except Exception as e:
            self.get_logger().error(f"Ошибка обработки кадра: {str(e)}")

        self.data_pub.publish(pose_msg)
        self.is_catched = False

def main(args=None):
    rclpy.init(args=args)
    node = CameraTrackingNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()
