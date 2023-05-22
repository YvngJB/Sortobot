# server.py - send rgb data

import socket

class Server:
    def __init__(self, port: int, callback: "function") -> None:
        self.callback = callback
        self.connection = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip = socket.gethostbyname(socket.gethostname())
        ip = "0.0.0.0"
        self.s.bind((ip, port))
        self.s.listen()
        print(f"[+] server listening on {ip}:{port}")

    def _handle_connection(self, connection: dict):
        while True:
            data = connection["connection"].recv(3).decode("ascii")
            if len(data) > 0:
                print(f"[+] message received: {data}")
                if data == "get":
                    msg = self.callback()
                    print(f"[+] sending callback value: {msg}")
                    connection["connection"].send(bytes(msg, "ascii"))

    def run(self):
        while True:
            connection = {}
            connection["connection"], connection["address"] = self.s.accept()
            print(f"[+] connection from {connection['address']}")
            self._handle_connection(connection)