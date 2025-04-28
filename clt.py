import cv2
import numpy as np
import mss
import socket
import pyautogui  # 用於控制滑鼠
import threading

SERVER_IP = '192.168.47.1'  # 替換為伺服器的 IP
PORT = 12345             # 與伺服器的埠號一致
# 建立兩個全局旗標
connected_event = threading.Event()  # 連線成功的旗標
stop_event = threading.Event()       # 停止線程的旗標

def screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # [1] 表示主螢幕

        # 擷取螢幕
        screenshot = sct.grab(monitor)

        # 將擷取的影像轉換為 NumPy 陣列
        img = np.array(screenshot)

        # 將影像從 BGRA 轉換為 BGR（OpenCV 使用 BGR 格式）
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # 壓縮影像為 JPEG 格式
        _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])  # 壓縮品質 50%
        return buffer.tobytes()
def ShowDisPlayToBack(client_socket):
    try:
        print("開始發送螢幕擷取影像...")
        while True:
            print("開始發送螢幕擷取影像...")
            while True:
                # 擷取並壓縮影像
                message = screenshot()
                # 傳送影像大小（先傳送資料長度）
                client_socket.sendall(len(message).to_bytes(4, 'big'))

                # 傳送影像資料
                client_socket.sendall(message)
                
    except socket.timeout:
        print("Socket 超時，停止發送影像")
    except Exception as e:
        print(f"發送影像時發生錯誤: {e}")
    finally:
        print("停止發送螢幕擷取影像")
            
def CltMoes(client_socket):
    while True:
        try:
            print("開始接收滑鼠點擊指令...")
            command_type = client_socket.recv(1).decode('utf-8')  # 接收指令類型
            if command_type == 'C':  # 'C' 表示滑鼠點擊
                coords = client_socket.recv(8)  # 接收滑鼠座標 (x, y)
                x, y = int.from_bytes(coords[:4], 'big'), int.from_bytes(coords[4:], 'big')
                screen_width, screen_height = pyautogui.size()
                if 0 <= x < screen_width and 0 <= y < screen_height:
                    pyautogui.click(x, y)
                    print(f"滑鼠點擊座標: ({x}, {y})")
                else:
                    print(f"座標 ({x}, {y}) 超出螢幕範圍，無法點擊")
        except Exception as e:
            print(f"接收指令時發生錯誤: {e}")
        finally:
            print("停止接收滑鼠點擊指令")
if __name__ == "__main__":
    while True:
        try:
            print("連線中...")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            client_socket.connect((SERVER_IP, PORT))
            print(f"已連線到伺服器 {SERVER_IP}:{PORT}")
            connected_event.set()
            client_socket.settimeout(100)  # 設定 timeout
            # 啟動線程
            thread1 = threading.Thread(target=ShowDisPlayToBack, args=(client_socket,))
            thread2 = threading.Thread(target=CltMoes, args=(client_socket,))
            thread1.start()
            thread2.start()

            # 等待線程結束
            thread1.join()
            thread2.join()

        except socket.timeout:
            print("Socket 連線超時，重新嘗試")
        except socket.error as e:
            print(f"Socket 連線錯誤: {e}")
        except KeyboardInterrupt:
            print("中斷連線")
            break
        finally:
            stop_event.set()
            connected_event.clear()
            try:
                client_socket.close()
            except:
                pass