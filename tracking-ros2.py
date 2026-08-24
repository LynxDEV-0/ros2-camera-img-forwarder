import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class CameraTrackingNode(Node):
    def __init__(self):
        super().__init__('img_processor')

        # Паблишер для отправки координат
        self.data_pub = self.create_publisher(Pose2D, '/camera/tracking_coords', 25)

        # Конвертер из ROS Image в OpenCV
        self.bridge = CvBridge()

        # Подписка на топик с видеопотоком
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.is_catched = False

    def image_callback(self, msg):
        try:
            # Конвертируем ROS-сообщение в картинку OpenCV
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # ТЕСТ: Выводим окно с видео прямо из топика Ubuntu
            cv2.imshow("WSL ROS Topic Viewer", frame)
            cv2.waitKey(1)

            # Переменные для координат объекта
            xcor = 0.0
            ycor = 0.0

            # TODO: Здесь будет ваш алгоритм OpenCV для поиска (например, красного куба)
            # Если объект найден:
            # self.is_catched = True
            # xcor = найденный_x
            # ycor = найденный_y

            # Формируем и отправляем координаты в ROS
            pose_msg = Pose2D()
            pose_msg.x = float(xcor)
            pose_msg.y = float(ycor)
            pose_msg.theta = 1.0 if self.is_catched else 0.0

            self.data_pub.publish(pose_msg)
            self.is_catched = False # Сброс флага для следующего кадра

        except Exception as e:
            self.get_logger().error(f"Ошибка обработки кадра: {str(e)}")

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
