import threading
from proxy_utils import recv_data, get_path, add_path_cookie, get_Cookie


class ResponseThread(threading.Thread):
    def __init__(self, conn, addr, byte_size, connections: list):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.byte_size = byte_size
        self.connections = connections
        self.headers = None
        self.body = None

    def run(self):
        self.headers, self.body = recv_data(self.conn, self.addr, self.byte_size)
        try:
            self.detected_cookie_path =  get_path(self.headers)[1].encode('utf-8').removesuffix(b'\r')
        except AttributeError:
            print("❌Cookie")
        finally:
            self.detected_url_path = get_path(self.headers)[0].encode('utf-8').removesuffix(b'\r')
        self.new_path_flag = False
        for i in self.connections:
            if i.path == self.detected_url_path:
                self.detected_path = self.detected_url_path
                self.new_path_flag = True
                break
        if not self.new_path_flag:
            self.detected_path = self.detected_cookie_path
        for i in self.connections:
            if i.path == self.detected_path:
                self.headers, self.body = i.forward_request(self.headers + self.body)
    #handle no path match
        self.headers = add_path_cookie(self.headers, self.detected_path)
        self.conn.send(self.headers + self.body)
        self.conn.close()
        return

if __name__ == "__main__":
    print("Class defining responder")
