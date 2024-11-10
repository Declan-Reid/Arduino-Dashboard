import socket
import os

server_ip = "141.147.99.65"
server_port = 4269

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_ip, server_port))
    s.sendall(b"press_button")
    s.close()
