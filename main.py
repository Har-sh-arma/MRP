import socket


forward_ADDR = "127.0.0.1"
forward_PORT = 8000
bind_ADDR = "127.0.0.1"
bind_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((bind_ADDR, bind_PORT))
sock.listen(20)

print("Listening...")

while True:
    print("Waiting for connection...")
    conn, addr = sock.accept()
    try:
        with conn:
            print(f"Request Received from {addr[0]}:{addr[1]}")
            data=b''
            while True:
                data1 = conn.recv(1024)
                data += data1
                if not data1:
                    break
            clienTsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clienTsock.connect((forward_ADDR, forward_PORT))
            clienTsock.send((data.decode("utf-8").replace(f"Host: {bind_ADDR}:{bind_PORT}", f"Host: {forward_ADDR}:{forward_PORT}").replace(f"Referer: {bind_ADDR}:{bind_PORT}", f"Referer: {forward_ADDR}:{forward_PORT}")).encode("utf-8"))
            print(f"Request Forwarded to {forward_ADDR}:{forward_PORT}")
            data = b''
            while True:
                data1 = clienTsock.recv(1024)
                data += data1
                if not data1:
                    break
            clienTsock.close()
            conn.send(data)
            print(f"Response Sent to {addr[0]}:{addr[1]}\n\n\n")
    except Exception as e:
        print(e)
