import socket

class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((self.host, self.port))
        print(f"[+] connected to {self.host}:{self.port}")

    def send_request(self):
        request = "get"
        self.s.sendall(request.encode("ascii"))
        print(f"[+] request sent: {request}")

    def receive_response(self):
        response = self.s.recv(1024).decode("ascii")
        print(f"[+] response received: {response}")
        return response

    def close(self):
        self.s.close()


if __name__ == "__main__":
    client = Client("localhost", 5678)  # Customize Host and Port
    client.connect()

    client.send_request()

    response = client.receive_response()
    # Handle received answer

    client.close()
