# Если не работает, открой порт c помощью Windows PowerShell:
# New-NetFirewallRule -DisplayName "WSL UDP Camera Port" -Direction Inbound -Action Allow -Protocol UDP -LocalPort 5005

import cv2
import socket

WSL_IP = "172.26.59.109" # указать IP WSL (узнать через hostname -I в WSL)
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)

print("Запуск передачи видео в WSL.")

try:
        while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                        break

                frame = cv2.resize(frame, (640, 480))

                encoded, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                data = buffer.tobytes()

                if len(data) > 65500: continue

                sock.sendto(data, (WSL_IP, PORT))

                cv2.imshow('Windows Camera', frame) # локальный вывод (можно убрать)
                if cv2.waitKey(1) & 0xFF == ord('q'): break

except KeyboardInterrupt:
        pass

finally:
        cap.release()
        cv2.destroyAllWindows()
        sock.close()