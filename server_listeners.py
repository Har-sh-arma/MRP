import threading
import socket
import re
from proxy_utils import recv_data
'''
define a class that listens on a tcp port off the main thread
'''

class ServerListener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.path = None

    def run(self):
        print(f"Listening on port {self.port} on thread {threading.get_ident()}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(5)
        while True:
            self.conn, self.addr = sock.accept()
            self.handler()

    def handler(self):
        data = self.conn.recv(1024)
        if (self.authorize(data)):
            print(f"Connection Proxy Client from {self.addr[0]}:{self.addr[1]}")
            self.path = re.search(b'Path:(.*)', data).group(1)
        else:
            print("Unauthorized")
            self.conn.close()
    
    def forward_request(self, data):
        print("Remote Server ---> Client")
        self.conn.send(data)
        headers, body = recv_data(self.conn, self.addr, 1024)
        print("Remote Server <--- Client")
        return headers, body
        

    def authorize(self, data):
        #implement the auth anyway
        return True

if __name__ == '__main__':
    print("Class defining server listeners")

