import socket
import cv2
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor

class Server:
    def __init__(self, host='0.0.0.0', port=12345, max_workers=5):
        self.host = host
        self.port = port
        self.server_socket = None
        self.connections = []  # 存儲所有連線的列表
        self.addresses = []  # 存儲所有連線的地址
        self.control_enabled = True
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        # 按鈕座標
        self.button_top_left_x = 10
        self.button_top_left_y = 10
        self.button_bottom_right_x = 110
        self.button_bottom_right_y = 50

    def start_server(self):
        """啟動伺服器並開始接受連線"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # 允許最多5個連線
        #print(f"伺服器已啟動，正在等待連線...")

        threading.Thread(target=self._accept_connections).start()

    def _accept_connections(self):
        """接受新的客戶端連線並使用 ThreadPoolExecutor 處理"""
        while self.control_enabled:
            try:
                connection, address = self.server_socket.accept()
            except Exception as e:
                #print(f"接受連線時發生錯誤: {e}")
                continue
            #print(f"新客戶端連線：{address}")
            self.connections.append(connection)
            self.addresses.append(address)

            # 使用 ThreadPoolExecutor 提交客戶端處理任務
            self.executor.submit(self.handle_client, connection, address)

    def handle_client(self, connection, address):
        """處理客戶端的基礎邏輯（可擴展）"""
        #print(f"正在處理客戶端：{address}")
        try:
            while self.control_enabled:
                try:
                    connection.sendall(b'')  # 保持連線活躍
                    pass
                except socket.error as e:
                    # 處理連線中斷的情況
                    #print(f"與客戶端 {address} 的連線中斷: {e}")
                    break
                except Exception as e:
                    #print(f"處理客戶端 {address} 時發生其他錯誤: {e}")
                    break
        finally:
            self.remove_connection(connection, address)

    def remove_connection(self, connection, address):
        """移除已斷開的連線"""
        if connection in self.connections:
            self.connections.remove(connection)
        if address in self.addresses:
            self.addresses.remove(address)
        try:
            connection.close()
        except OSError as e:
            # 處理關閉已關閉 socket 的情況
            pass
        # print(f"客戶端 {address} 已斷開。")

    def get_connected_users(self):
        """返回當前連線的用戶地址列表"""
        return self.addresses

    def notify_user_to_start(self, user_address):
        """通知選定的用戶開始接收資料"""
        try:
            index = self.addresses.index(user_address)
            connection = self.connections[index]
            try:
                connection.sendall(b'START')  # 發送啟動信號
            except Exception as e:
                # print(f"通知用戶 {user_address} 開始接收時發生錯誤: {e}")
                pass
        except ValueError:
            # print(f"用戶 {user_address} 不在連線列表中。")
            pass

    def monitor_user(self, user_address):
        """監控選定用戶的螢幕畫面"""
        try:
            index = self.addresses.index(user_address)
            connection = self.connections[index]

            cv2.namedWindow("Live Screenshot", cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("Live Screenshot", self.mouse_callback, connection)

            try:
                while self.control_enabled:
                    try:
                        data_size = int.from_bytes(connection.recv(4), 'big')
                        if data_size <= 0 or data_size > 10**7:
                            # print("接收到的資料大小不合理")
                            continue

                        data = b''
                        while len(data) < data_size:
                            packet = connection.recv(min(4096, data_size - len(data)))
                            if not packet:
                                # print(f"客戶端 {user_address} 斷開連線")
                                break
                            data += packet

                        if not data:
                            continue

                        img_array = np.frombuffer(data, dtype=np.uint8)
                        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                        if img is None:
                            # print("接收影像失敗")
                            continue

                        cv2.imshow("Live Screenshot", img)

                        if cv2.waitKey(1) & 0xFF == 27:  # 按下 ESC 鍵退出監控
                            break
                    except socket.error as e:
                        # print(f"與客戶端 {user_address} 的連線中斷: {e}")
                        break
                    except ValueError:
                        # print("接收到的資料大小轉換錯誤。")
                        break
                    except Exception as e:
                        # print(f"監控用戶 {user_address} 時發生其他錯誤: {e}")
                        break
            finally:
                cv2.destroyAllWindows()
                # print(f"停止監控用戶: {user_address}")
        except ValueError:
            # print(f"用戶 {user_address} 不在連線列表中。")
            if 'Live Screenshot' in cv2.getWindowImageRect('Live Screenshot'):
                cv2.destroyWindow('Live Screenshot')
        except Exception as e:
            # print(f"監控用戶 {user_address} 時發生錯誤: {e}")
            if 'Live Screenshot' in cv2.getWindowImageRect('Live Screenshot'):
                cv2.destroyWindow('Live Screenshot')

    def mouse_callback(self, event, x, y, flags, connection):
        """處理滑鼠事件並向客戶端發送滑鼠控制指令"""
        if event == cv2.EVENT_LBUTTONDOWN:  # 滑鼠左鍵點擊
            try:
                connection.sendall(b'C')  # 發送滑鼠控制指令
                connection.sendall(x.to_bytes(4, 'big') + y.to_bytes(4, 'big'))  # 傳送滑鼠座標
                # print(f"滑鼠點擊座標: ({x}, {y})")
            except Exception as e:
                # print(f"滑鼠控制指令發送失敗: {e}")
                pass

    def cleanup(self):
        """清理所有連線並關閉伺服器"""
        self.control_enabled = False
        if self.server_socket:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass  # Socket 可能已經關閉
            self.server_socket.close()
        for conn in self.connections:
            try:
                conn.close()
            except OSError:
                pass  # Socket 可能已經關閉
        self.executor.shutdown(wait=False)  # 不等待所有任務完成
        cv2.destroyAllWindows()
        # print("伺服器已關閉。")

    def nowuser(self):
        """返回當前連線的客戶端數量"""
        return self.connections

    def run(self):
        try:
            self.start_server()
            # 保持主線程運行，以便在需要時進行清理
            while True:
                try:
                    import time
                    time.sleep(1)
                except KeyboardInterrupt:
                    break
        finally:
            self.cleanup()

if __name__ == '__main__':
    server = Server()
    server.run()
