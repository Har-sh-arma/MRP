'''

\r Crap is for Windows based systems should not bother on linux tho


Client service for the Reverse Proxy

tcp socket to the proxy server receives the http reqs
changes the headers to request the local server

captures response and sends it to the proxy server
'''

import socket
import re
from proxy_utils import recv_data, get_path

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 1001
byte_size = 32
ASSIGNED_PATH = "/abc"
LOCAL_SERVER = "127.0.0.1"
LOCAL_PORT = 8000

# handle local server crash and re establish connection

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((SERVER_ADDR, SERVER_PORT))
sock.send(b"Path:" + ASSIGNED_PATH.encode('utf-8'))
print("Connection Init")
while True:
    headers, body = recv_data(sock, (SERVER_ADDR, SERVER_PORT), byte_size)
    print("Client <-- remote Server")

    detected_path = get_path(headers).encode('utf-8').removesuffix(b'\r')
    if detected_path == ASSIGNED_PATH.encode('utf-8'):
        headers = re.sub(ASSIGNED_PATH.encode('utf-8'), b"/", headers)

    local_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_sock.connect((LOCAL_SERVER, LOCAL_PORT))
    local_sock.send(headers + body)
    print("local server <-- Client")
    
    resp_headers, resp_body = recv_data(local_sock, (LOCAL_SERVER, LOCAL_PORT), byte_size)
    local_sock.close()
    print("local server --> Client")
    
    resp = resp_headers + resp_body
    sock.send(resp)
    print("Client --> remote Server")


