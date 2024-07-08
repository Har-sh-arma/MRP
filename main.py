'''
Server service for the Reverse Proxy
'''

import socket
import re
from server_listeners import ServerListener
from proxy_utils import recv_data, get_path, add_path_cookie, get_Cookie


def print_utf(inp):
    print(f"\n{inp.decode('utf-8')}")


print("Initializing sockets for the proxy client to connect to...")
connections = []

for i in range(1000, 1005):
    listener = ServerListener(i)
    connections.append(listener)
    listener.start()

bind_ADDR = "127.0.0.1"
bind_PORT = 1234
byte_size = 32


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((bind_ADDR, bind_PORT))
sock.listen()
print("Listening...")



while True:
    conn, addr = sock.accept()
    headers, body = recv_data(conn, addr, byte_size)
    detected_path = get_path(headers).encode('utf-8').removesuffix(b'\r')
    print(f"Detected path: {detected_path}")

    for i in connections:
        if i.path == detected_path:
            headers, body = i.forward_request(headers + body)
        #handle no path match
    headers = add_path_cookie(headers, detected_path)
    conn.send(headers + body)
    conn.close()

