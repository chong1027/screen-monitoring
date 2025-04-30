import socket
import cv2
import numpy as np
import sys
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.connections = []  # 用來存儲所有連線的列表
        self.control_enabled = True

        # 按鈕座標
        self.button_top_left_x = 10
        self.button_top_left_y = 10
        self.button_bottom_right_x = 110
        self.button_bottom_right_y = 50

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # 允許最多5個連線
        print(f"伺服器已啟動，正在等待連線...")

        while True:
            # 等待客戶端連線
            connection, address = self.server_socket.accept()
            print(f"新客戶端連線：{address}")
            self.connections.append(connection)  # 把新連線加入列表

            # 創建新的線程來處理這個連線
            client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
            client_thread.start()

    def handle_client(self, connection, address):
        cv2.namedWindow("Live Screenshot", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Live Screenshot", self.mouse_callback)

        try:
            while True:
                data_size = int.from_bytes(connection.recv(4), 'big')
                if data_size <= 0 or data_size > 10**7:
                    print("接收到的資料大小不合理")
                    break

                data = b''
                while len(data) < data_size:
                    packet = connection.recv(min(4096, data_size - len(data)))
                    if not packet:
                        print(f"客戶端 {address} 斷開連線")
                        break
                    data += packet

                if not data:
                    break

                img_array = np.frombuffer(data, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is None:
                    print("接收影像失敗")
                    break

                # 畫按鈕
                button_color = (0, 255, 0) if self.control_enabled else (0, 0, 255)
                cv2.rectangle(img, (self.button_top_left_x, self.button_top_left_y), (self.button_bottom_right_x, self.button_bottom_right_y), button_color, -1)
                cv2.putText(img, "Control" if self.control_enabled else "Disable",
                            (self.button_top_left_x + 5, self.button_top_left_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                # 畫 Exit 按鈕
                cv2.rectangle(img, (self.button_top_left_x + 160, self.button_top_left_y), (self.button_bottom_right_x + 160, self.button_bottom_right_y), (255, 0, 0), -1)
                cv2.putText(img, "Exit",
                            (self.button_top_left_x + 210, self.button_top_left_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                cv2.imshow("Live Screenshot", img)

                if cv2.waitKey(1) & 0xFF == 27:
                    break

        except Exception as e:
            print(f"處理客戶端 {address} 時發生錯誤: {e}")
        finally:
            connection.close()
            self.connections.remove(connection)  # 斷開後移除該連線
            print(f"客戶端 {address} 已斷開連線")

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.button_top_left_x <= x <= self.button_bottom_right_x and self.button_top_left_y <= y <= self.button_bottom_right_y:
                self.control_enabled = not self.control_enabled
                print(f"控制模式 {'啟用' if self.control_enabled else '停用'}")

            elif self.button_top_left_x + 160 <= x <= self.button_bottom_right_x + 160 and self.button_top_left_y <= y <= self.button_bottom_right_y:
                print("退出伺服器")
                self.cleanup()
                sys.exit(0)

            elif self.control_enabled:
                print(f"滑鼠點擊座標: ({x}, {y})")
                for conn in self.connections:  # 發送到所有連線的客戶端
                    try:
                        conn.sendall(b'C')
                        conn.sendall(x.to_bytes(4, 'big') + y.to_bytes(4, 'big'))
                    except Exception as e:
                        print(f"傳送滑鼠座標失敗: {e}")

    def cleanup(self):
        # 關閉所有連線
        for conn in self.connections:
            conn.close()
        if self.server_socket:
            self.server_socket.close()
        cv2.destroyAllWindows()
        print("伺服器已關閉。")

    def run(self):
        try:
            self.start_server()
        finally:
            self.cleanup()

