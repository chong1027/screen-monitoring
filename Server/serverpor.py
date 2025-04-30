from api.SmartMenu import SmartMenu
from services import Server
if __name__ == "__main__":
    options = ["選項 1", "選項 2", "選項 3"]
    menu = SmartMenu(options)  # 實例化 SmartMenu 類別
    choe = menu.show()  # 等待用戶選擇
    
    host = '0.0.0.0'
    port = 12345
    server = Server(host, port)
    server.run()
