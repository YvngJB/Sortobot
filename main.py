from server import Server
from cam import Camera

if __name__ == "__main__":
    cam = Camera()
    server = Server(5678, cam.scan)
    server.run()