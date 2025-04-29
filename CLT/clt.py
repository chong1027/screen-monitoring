import asyncio
import mss
import numpy as np
import cv2
import pyautogui

SERVER_IP = '192.168.47.1'
PORT = 12345

def screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])
        return buffer.tobytes()

async def send_screen(writer):
    print("開始傳送螢幕影像")
    while True:
        try:
            data = screenshot()
            length = len(data).to_bytes(4, 'big')
            writer.write(length + data)
            await writer.drain()
            await asyncio.sleep(0.05)  # 降低頻率，避免塞爆
        except Exception as e:
            print("傳送錯誤:", e)
            break

async def recv_mouse(reader):
    print("開始接收滑鼠指令")
    try:
        while True:
            command_type = await reader.readexactly(1)
            if command_type == b'C':
                coords = await reader.readexactly(8)
                x = int.from_bytes(coords[:4], 'big')
                y = int.from_bytes(coords[4:], 'big')
                screen_width, screen_height = pyautogui.size()
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
while True:
    asyncio.run(main())
