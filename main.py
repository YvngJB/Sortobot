# main.py

from datetime import datetime
from mongomaster import MongoMaster
from scan import Scan
from client_cam import Client
# from client_temp import OPCUAClient
from robot import Robot
import calendar
import time
from watty import get_prices
from config import IP_CAM, IP_PC, IP_SRV, IP_TEMP

if __name__ == "__main__":
    # setup monogdb controller
    mongomaster = MongoMaster(f"mongodb://{IP_SRV}:27017")
    mongomaster.switch_database("robby")
    mongomaster.switch_collection("scans")

    # setup robot
    robot = Robot()

    # setup camera socket client
    camera = Client(IP_CAM, 5678)
    camera.connect()

    # setup temperature client
    # opcua = OPCUAClient()
    # opcua.connect(IP_TEMP)

    # main loop
    while True:
        try:
            input("Press [ENTER] to scan.")

            # create current timestamp
            timestamp = calendar.timegm(time.gmtime())

            # robot pickup
            print("[+] moving to pickup")
            robot.move_home()
            robot.move_pickup_xy()
            robot.move_pickup_z()
            robot.suction()
            
            # robot move camera
            print("[+] moving to camera")
            robot.move_camera_xy()
            robot.move_camera_z()
           
            # camera scan
            print("[+] scanning...")
            color = camera.scan()
            print("[+] go color: ", color)

            # temperature scan
            #temperature = opcua.pull("ns=2;i=3")

            # humidity scan
            # humidity = opcua.pull("ns=2;i=4")
            
            # move cube to box
            print("[+] moving cube to box")
            robot.move_pickup_xy()
            robot.move_home()
            if color == "r":
                robot.move_red_xyz()
            elif color == "g":
                robot.move_green_xyz()
            elif color == "b":
                robot.move_blue_xyz()
            robot.suction()
            robot.move_home()

            # create end timestamp
            end_timestamp = calendar.timegm(time.gmtime())

            #duration
            duration = abs(int((datetime.fromtimestamp(timestamp) - datetime.fromtimestamp(end_timestamp)).total_seconds()))

            # costs
            marketprices = get_prices()
            price = marketprices[0].marketprice / 1000
            cost = (round(1.2 * price, 2) / 3600) * duration # cost per kilowatt sekunde 
            cost = round(cost, 5)

            # color
            if color == "r":
                color = "red"
            elif color == "b":
                color = "blue"
            elif color == "g":
                color = "green"

            # create scan object
            #scan = Scan(controller.get_next_id(), timestamp, color, temperature, humidity, duration, cost)

            # add scan to database
            #
            # controller.add_scan(scan)
        except KeyboardInterrupt:
            # opcua client needs to disconnect
            opcua.disconnect()
            print("Bye!")
        except:
            raise