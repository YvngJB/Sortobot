from camserver import Camserver
from camv2 import Camera
from opcuaserver import Opcuaserver

if __name__ == "__main__":
    cam = Camera()
    camserver = Camserver(65432, cam.scan)
    camserver.run()
    opcuaserver = Opcuaserver()
    opcuaserver.run()
