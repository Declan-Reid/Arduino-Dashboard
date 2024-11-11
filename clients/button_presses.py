import socket
import time
import os

server_ip = "arduino.declan-reid.me"
server_port = 2052

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            s.sendall(b"get_button_count")
            data = s.recv(1024)

        print(f"\r{data.decode()}", end="")
        for i in range(os.get_terminal_size()[0] - len(data.decode())):
            print(" ", end="")

        # time.sleep(1)
    except KeyboardInterrupt:
        exit()
    except:
        continue
