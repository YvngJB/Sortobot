from cam_server import Server
from camv2 import Camera

if __name__ == "__main__":
    cam = Camera()
    server = Server(5678, cam.scan)
    server.run()