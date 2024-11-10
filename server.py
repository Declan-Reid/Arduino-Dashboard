import socket
import json
import datetime

button_count = 0

minecraft_server = {
    'name': 'MoldyyBox Dev Server',
    'status_colour': 'red',
    'Player Max': 'N/A',
    'Player Count': 'N/A',
    'MOTD': 'N/A',
}

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 2052))
s.listen()

try:
    while True:
        c, addr = s.accept()
        data = c.recv(1024)
        request_value = data.decode()
        
        print('Recieved packet from: ' + addr[0])
        print('Request: ' + request_value)
        print()

        request_data = request_value.split(';')

        print(request_data[0])

        match request_data[0]:
            case "press_button":
                button_count += 1
                pass

            case "get_button_count":
                c.send(str(button_count).encode())

            case "set_minecraft_server_data":
                minecraft_server['status_colour'] = 'green'
                minecraft_server['Player Max'] = request_data[1]
                minecraft_server['Player Count'] = request_data[2]
                minecraft_server['MOTD'] = request_data[3]
                pass

            case "minecraft_server_close":
                minecraft_server['status_colour'] = 'red'
                minecraft_server['Player Max'] = 'N/A'
                minecraft_server['Player Count'] = 'N/A'
                minecraft_server['MOTD'] = 'N/A'
                pass
                

            case "get_all_panels":
                minecraft_server_body = {
                    'name': minecraft_server['name'],
                    'status_colour': minecraft_server['status_colour'],
                    'Players': minecraft_server['Player Count'] + ' / ' + minecraft_server['Player Max'] if minecraft_server['Player Count'] != "N/A" else "N/A",
                    'MOTD': minecraft_server['MOTD'],
                }

                body = [
                    json.dumps(minecraft_server_body),
                ]

                response = json.dumps({
                    'timestamp': int(datetime.datetime.now().timestamp()),
                    'request': request_value,
                    'body': body,
                })

                c.send(response.encode())
            case _:
                c.send("invalid".encode())

        c.close()
except Exception as e:
    s.close()
    raise e