import socket
import cv2
import numpy as np

# 設定伺服器的 IP 和埠號
HOST = '0.0.0.0'  # 接受來自所有網路介面的連線
PORT = 12345      # 使用的埠號

# 建立 Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"伺服器已啟動，正在等待連線...")

# 接受客戶端連線
conn, addr = server_socket.accept()
conn.settimeout(5)  # 設定接收資料的超時時間
print(f"已連線：{addr}")

# 創建 OpenCV 視窗
cv2.namedWindow("Live Screenshot", cv2.WINDOW_NORMAL)

# 控制模式旗標
control_enabled = True
continue_edabled = False
# 定義按鈕區域
button_x1, button_y1 = 10, 10  # 按鈕左上角座標
button_x2, button_y2 = 110, 50  # 按鈕右下角座標

def mouse_callback(event, x, y, flags, param):
    global control_enabled
    if event == cv2.EVENT_LBUTTONDOWN:
        # 檢查是否點擊了按鈕
        if button_x1 <= x <= button_x2 and button_y1 <= y <= button_y2:
            control_enabled = not control_enabled
            print(f"控制模式 {'啟用' if control_enabled else '停用'}")
        elif button_x1+160 <= x <= button_x2+160 and button_y1 <= y <= button_y2:
            # 如果點擊了退出按鈕，關閉伺服器
            print("退出伺服器")
            conn.close()
            server_socket.close()
            cv2.destroyAllWindows()
            exit(0)
        elif control_enabled:
            # 如果控制模式啟用，傳送滑鼠點擊座標
            print(f"滑鼠點擊座標: ({x}, {y})")
            try:
                conn.sendall(b'C')  # 傳送指令類型 'C'
                conn.sendall(x.to_bytes(4, 'big') + y.to_bytes(4, 'big'))  # 傳送座標
                print(f"傳送滑鼠點擊座標: ({x}, {y})")
            except socket.error as e:
                print(f"傳送滑鼠點擊座標失敗: {e}")
            except Exception as e:
                print(f"無法傳送滑鼠點擊座標: {e}")

cv2.setMouseCallback("Live Screenshot", mouse_callback)

while True:
    try:
        # 接收影像大小
        data_size = int.from_bytes(conn.recv(4), 'big')
        if data_size <= 0 or data_size > 10**7:
            print("接收到的資料大小不合理")
            break

        # 接收影像資料
        data = b''
        while len(data) < data_size:
            packet = conn.recv(min(4096, data_size - len(data)))
            if not packet:
                print("接收資料失敗，可能是連接中斷")
                break
            data += packet

        if not data:
            break

        # 將影像資料轉換為 NumPy 陣列並解碼
        img_array = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            print("接收影像失敗")
            break

        # 繪製按鈕
        button_color = (0, 255, 0) if control_enabled else (0, 0, 255)
        cv2.rectangle(img, (button_x1, button_y1), (button_x2, button_y2), button_color, -1)
        cv2.putText(img, "Control" if control_enabled else "Disable", 
                    (button_x1 + 5, button_y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(img, (button_x1+160, button_y1), (button_x2+160, button_y2), (255,0,0), -1)
        cv2.putText(img, "Exit",  
                    (button_x1 + 210, button_y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        # 顯示影像
        cv2.imshow("Live Screenshot", img)
        

        # 檢查是否按下 ESC 鍵退出
        if cv2.waitKey(1) & 0xFF == 27:
            break

    except socket.timeout:
        print("接收資料超時，重新嘗試")
        continue
    except Exception as e:
        print(f"發生錯誤: {e}")
        break

conn.close()
server_socket.close()
cv2.destroyAllWindows()
print("伺服器已關閉。")