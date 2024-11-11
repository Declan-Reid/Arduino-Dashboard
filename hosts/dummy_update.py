import socket
import os

server_ip = "arduino.declan-reid.me"
server_port = 2052

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_ip, server_port))
    s.sendall(b"press_button")
    s.close()
