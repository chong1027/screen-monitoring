import asyncio
from mss import mss
import numpy as np
import cv2
import pyautogui

SERVER_IP = '192.168.47.1'
PORT = 12345

# 設定螢幕傳輸解析度
def screenshot():
    while True:
        with mss() as sct:
            # 設定螢幕區域，這裡使用第一個螢幕
            monitor = sct.monitors[1]
            # 將螢幕影像轉換為 NumPy 陣列
            # 這裡使用 BGRA 格式，然後轉換為 BGR 格式
            img = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2BGR)
            # 將影像轉換為 JPEG 格式並壓縮
            _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])

            # buffer 可能為 None，這是正常的
            # 因為在某些情況下，影像可能無法正確捕捉
            # 這裡我們檢查 buffer 是否為 None
            # 如果是 None，則繼續捕捉
            # 否則返回 buffer 的 bytes 形式
            if buffer is None:
                continue
            
            return buffer.tobytes()
# 螢幕影像傳輸
# 使用 asyncio 實現非同步傳輸
async def send_screen(writer):
    print("開始傳送螢幕影像")
    while True:
        try:
            data = screenshot()
            length = len(data).to_bytes(4, 'big')
            # 將影像長度轉換為 4 個位元組的 bytes
            # 並將影像資料與長度一起傳送
            writer.write(length + data)
            # 等待傳送完成
            # 這裡使用 drain() 方法來確保所有資料都已傳送
            await writer.drain()
            await asyncio.sleep(0.05)  # 降低頻率，避免塞爆
        except Exception as e:
            print("傳送錯誤:", e)
            break
# 接收滑鼠指令
# 使用 asyncio 實現非同步接收
async def recv_mouse(reader):
    print("開始接收滑鼠指令")
    try:
        while True:
            # 讀取 1 個位元組的指令類型
            # 這裡使用 readexactly() 方法來確保讀取到正確的位元組數量
            command_type = await reader.readexactly(1)
            # 如果指令類型為 b'C'，則讀取 4 個位元組的滑鼠位置
            if command_type == b'C':
                # 讀取 8 個位元組的滑鼠位置
                # 這裡使用 readexactly() 方法來確保讀取到正確的位元組數量
                coords = await reader.readexactly(8)
                # 將滑鼠位置的前 4 個位元組轉換為 x 座標
                # 將後 4 個位元組轉換為 y 座標
                x = int.from_bytes(coords[:4], 'big')
                y = int.from_bytes(coords[4:], 'big')
                # 將滑鼠位置轉換為整數
                screen_width, screen_height = pyautogui.size()
                # 並檢查是否在螢幕範圍內
                if 0 <= x < screen_width and 0 <= y < screen_height:
                    pyautogui.click(x, y)
                    print(f"滑鼠點擊: ({x}, {y})")
    except Exception as e:
        print("滑鼠接收錯誤:", e)

async def main():
    try:
        reader, writer = await asyncio.open_connection(SERVER_IP, PORT)
        print("已連線到伺服器")
        await asyncio.gather(
            send_screen(writer),
            recv_mouse(reader)
        )
    except Exception as e:
        print("連線錯誤:", e)
        
if __name__ == "__main__":
    while True:
        asyncio.run(main())
