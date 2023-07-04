from camserver import Camserver
from camv2 import Camera
from opcuaserver import Opcuaserver
from threading import Thread


if __name__ == "__main__":
    #starten des Kameraservers
    cam = Camera()
    camserver = Camserver(65432, cam.scan)
    
    #starten des Opcuaservers
    opcuaserver = Opcuaserver()
    camserver_thread = Thread(target=camserver.run)
    camserver_thread.start()
    opcuaserver.run()