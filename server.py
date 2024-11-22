import socket
import json
import datetime
import time
import os
import threading
import asyncio
import ssl
from websockets.server import serve, WebSocketServerProtocol
import socket

class Colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

ominous_button = {
    "name": "Ominous Button",
    "status": "Watching, as always.",
    "status_colour": "green",
    "last_updated": 0,
    "Button Presses": 0,
}

minecraft_server = {
    "name": "MoldyyBox Dev Server",
    "status": "Offline",
    "status_colour": "red",
    "last_updated": 0,
    "Player Max": "N/A",
    "Player Count": "N/A",
    "MOTD": "N/A",
}

pico_w_sensors = {
    "name": "Pico W Sensors",
    "status": "Offline",
    "status_colour": "red",
    "last_updated": 0,
    "Temperature": "N/A",
    "Barometric Pressure": "N/A",
    "Humidity": "N/A",
}

temperatures = [
    [23.45, 9997.98, 28.34],
    [24.45, 10004.61, 29.45],
    [26.82, 10006.84, 31.02],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 2052))
s.listen()

def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def do_server_thing():
    while True:
        try:
            c, addr = s.accept()
            data = c.recv(1024)
            request_value = data.decode()

            # print("Recieved packet from: " + addr[0])
            # print("Request: " + request_value)
            # print()

            request_data = request_value.split(";")

            match request_data[0]:
                case "press_button":
                    ominous_button["last_updated"] = int(datetime.datetime.now().timestamp())
                    ominous_button["Button Presses"] += 1
                    pass

                case "get_button_count":
                    c.send(str(ominous_button["Button Presses"]).encode())

                case "set_minecraft_server_data":
                    minecraft_server["status_colour"] = "green"
                    minecraft_server["status"] = "Online"
                    minecraft_server["last_updated"] = int(datetime.datetime.now().timestamp())
                    minecraft_server["Player Max"] = request_data[1]
                    minecraft_server["Player Count"] = request_data[2]
                    minecraft_server["MOTD"] = request_data[3]
                    pass

                case "minecraft_server_close":
                    minecraft_server["status_colour"] = "red"
                    minecraft_server["status"] = "Offline"
                    minecraft_server["Player Max"] = "N/A"
                    minecraft_server["Player Count"] = "N/A"
                    minecraft_server["MOTD"] = "N/A"
                    pass

                case "set_pico_w_sensors":
                    pico_w_sensors["status_colour"] = "green"
                    pico_w_sensors["status"] = "Online"
                    pico_w_sensors["last_updated"] = int(datetime.datetime.now().timestamp())
                    pico_w_sensors["Temperature"] = request_data[1]
                    pico_w_sensors["Barometric Pressure"] = request_data[2]
                    pico_w_sensors["Humidity"] = request_data[3]
                    pass

                case "get_all_panels":
                    minecraft_server_body = {
                        "name": minecraft_server["name"],
                        "status_colour": minecraft_server["status_colour"],
                        "status": minecraft_server["status"],
                        "Players": (
                            minecraft_server["Player Count"]
                            + " / "
                            + minecraft_server["Player Max"]
                            if minecraft_server["Player Count"] != "N/A"
                            else "N/A"
                        ),
                        "MOTD": minecraft_server["MOTD"],
                    }

                    pico_w_sensors_body = {
                        "name": pico_w_sensors["name"],
                        "status_colour": pico_w_sensors["status_colour"],
                        "status": pico_w_sensors["status"],
                        "Temperature": pico_w_sensors["Temperature"],
                        "Barometric Pressure": pico_w_sensors["Barometric Pressure"],
                        "Humidity": pico_w_sensors["Humidity"],
                    }

                    button_presses_body = {
                        "name": ominous_button["name"],
                        "status_colour": ominous_button["status_colour"],
                        "status": ominous_button["status"],
                        "Button Presses": str(ominous_button["Button Presses"]),
                    }

                    body = [
                        json.dumps(minecraft_server_body),
                        json.dumps(pico_w_sensors_body),
                        json.dumps(button_presses_body),
                    ]

                    response = json.dumps(
                        {
                            "timestamp": int(datetime.datetime.now().timestamp()),
                            "request": request_value,
                            "body": body,
                        }
                    )

                    c.send(response.encode())
                case _:
                    c.send("invalid".encode())

            c.close()
        except UnicodeDecodeError:
            print("Recieved invalid packet. Ignoring...")
        except ConnectionResetError:
            print("Socket closed unexpectedly. Expect madness to come.")
        except Exception as e:
            s.close()
            raise e

def update_things():
    while True:
        if minecraft_server["last_updated"] + 30 < int(datetime.datetime.now().timestamp()): # If it hasn't been updated for 30 seconds
            minecraft_server["status_colour"] = "red"
            minecraft_server["status"] = "Offline"
            minecraft_server["Player Max"] = "N/A"
            minecraft_server["Player Count"] = "N/A"
            minecraft_server["MOTD"] = "N/A"
        elif minecraft_server["last_updated"] + 5 < int(datetime.datetime.now().timestamp()): # If it hasn't been updated for 5 seconds
            minecraft_server["status_colour"] = "yellow"
            minecraft_server["status"] = "Not Responding"
            
        if pico_w_sensors["last_updated"] + 30 < int(datetime.datetime.now().timestamp()): # If it hasn't been updated for 30 seconds
            pico_w_sensors["status_colour"] = "red"
            pico_w_sensors["status"] = "Offline"
            pico_w_sensors["Temperature"] = "N/A"
            pico_w_sensors["Barometric Pressure"] = "N/A"
            pico_w_sensors["Humidity"] = "N/A"
        elif pico_w_sensors["last_updated"] + 5 < int(datetime.datetime.now().timestamp()): # If it hasn't been updated for 5 seconds
            pico_w_sensors["status_colour"] = "yellow"
            pico_w_sensors["status"] = "Not Responding"


        clear_screen()
        print(Colour.BOLD + minecraft_server["name"] + Colour.END + '\n'
            + 'Status: ' + getattr(Colour, minecraft_server["status_colour"].upper()) + minecraft_server["status"] + Colour.END + '\n'
            + 'Players: ' + (
                minecraft_server["Player Count"]
                + " / "
                + minecraft_server["Player Max"]
                if minecraft_server["Player Count"] != "N/A"
                else "N/A"
            ) + '\n'
            + 'MOTD: ' + minecraft_server["MOTD"] + '\n\n'
            
            + Colour.BOLD + pico_w_sensors["name"] + Colour.END + '\n'
            + 'Status: ' + getattr(Colour, pico_w_sensors["status_colour"].upper()) + pico_w_sensors["status"] + Colour.END + '\n'
            + 'Temperature: ' + pico_w_sensors["Temperature"] + '\n'
            + 'Barometric Pressure: ' + pico_w_sensors["Barometric Pressure"] + '\n'
            + 'Humidity: ' + pico_w_sensors["Humidity"] + '\n\n'
            
            + Colour.BOLD + ominous_button["name"] + Colour.END + '\n'
            + 'Status: ' + getattr(Colour, ominous_button["status_colour"].upper()) + ominous_button["status"] + Colour.END + '\n'
            + 'Button Presses: ' + str(ominous_button["Button Presses"]) + '\n',
        end='')

        time.sleep(0.5)



## WEBSOCKET SERVER ##

# WebSocket server configuration
server_address = "127.0.0.1"
server_port = 2052

server_host = "arduino.declan-reid.me"

# SSL configuration for WSS
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(
    certfile="/etc/letsencrypt/live/arduino.declan-reid.me/fullchain.pem",
    keyfile="/etc/letsencrypt/live/arduino.declan-reid.me/privkey.pem",
)

async def websocketRespond(websocket: WebSocketServerProtocol, path: str):
    # Check if the Host header is the expected domain
    if websocket.request_headers.get("Host") != f"{server_host}:2053":
        print(
            f"Connection denied: Invalid Host header. Expected {server_host} but got {websocket.request_headers.get('Host')}"
        )
        await websocket.close(
            code=4000
        )  # Close the connection with a specific code for "Bad Request"
        return

    print("Connection from: " + websocket.remote_address[0])

    async for message in websocket:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_address, server_port))
                s.sendall(message.encode())
                data = s.recv(1024)
                await websocket.send(data.decode())
        except ConnectionRefusedError:
            print(f"Failed to connect to internal server on port {server_port}")
            await websocket.send("error")
        except asyncio.exceptions.IncompleteReadError:
            return

async def websocketMain():
    # Run the WebSocket server with SSL encryption (WSS)
    async with serve(websocketRespond, "0.0.0.0", 2053, ssl=ssl_context):
        print("Listening on port 2053")
        await asyncio.get_running_loop().create_future()  # run forever

def runWebsocketServer():
    asyncio.run(websocketMain())



t1 = threading.Thread(target=do_server_thing)
t2 = threading.Thread(target=update_things)
t3 = threading.Thread(target=runWebsocketServer)

t1.start()
t2.start()
t3.start()