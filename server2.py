import asyncio
import ssl
from websockets.server import serve, WebSocketServerProtocol
import socket

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


async def respond(websocket: WebSocketServerProtocol, path: str):
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


async def main():
    # Run the WebSocket server with SSL encryption (WSS)
    async with serve(respond, "0.0.0.0", 2053, ssl=ssl_context):
        print("Listening on port 2053")
        await asyncio.get_running_loop().create_future()  # run forever


# Run the server
asyncio.run(main())
