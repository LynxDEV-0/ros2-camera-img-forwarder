import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import socket
import numpy as np
from cv_bridge import CvBridge

class ImageReceiverNode(Node):
    def __init__(self):
        super().__init__('wsl_camera_receiver')
        
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.bridge = CvBridge()

        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        
        self.frame_count = 0
        
        self.timer = self.create_timer(1.0 / 30.0, self.receive_and_publish)
        self.get_logger().info("ROS нода запущена и слушает порт 5005...")

    def receive_and_publish(self):
        try:
            self.sock.settimeout(0.03)
            data, addr = self.sock.recvfrom(65535)
            
            np_arr = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                ros_image = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                
                ros_image.header.stamp = self.get_clock().now().to_msg()
                ros_image.header.frame_id = "camera_link"
                
                self.publisher_.publish(ros_image) # публикация
                
                self.frame_count += 1
                if self.frame_count % 30 == 0:
                    self.get_logger().info(f"ROS-нода работает. Кадров принято: {self.frame_count}")
                    
        except socket.timeout:
            pass
        except Exception as e:
            self.get_logger().error(f"Ошибка обработки: {str(e)}")

    def destroy_node(self):
        self.sock.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ImageReceiverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
