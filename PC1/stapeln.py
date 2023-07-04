import sys
from datetime import datetime
import DoBotArm as Dbt
import socket
import pymongo
import time
import calendar
from opcua import Client
import math
from mongomaster import MongoMaster
from scan import Scan

#Funktion zum ermitteln der Ablagekoordinaten des würfels anhand der Anzahl Würfel die bereits auf seinem Farbstapel liegen
def nextDrop(stackNum , Xbase, Ybase, Zbase, cubeM):
    erg = [0,0,0]
    curLayerCubes = stackNum%4
    cubeM += 1
    if curLayerCubes <= 1:
        erg[0] = Xbase
        erg[1] = Ybase + (cubeM * curLayerCubes)
        erg[2] = Zbase + (cubeM * (math.floor(stackNum/4)))
    else:
        erg[0] = Xbase + cubeM
        erg[1] = Ybase + (cubeM * (curLayerCubes -2))
        erg[2] = Zbase + (cubeM * (math.floor(stackNum/4)))
    return erg

#Einrichten der Datenbankverbindung
mongomaster = MongoMaster(f"mongodb://10.100.20.146:27017")
mongomaster.switch_dbase("team7")
mongomaster.switch_collection("scans")

HOST = "192.168.187.2"  # Pi IP
#HOST = "10.62.255.2"  # Pi IP
CAMPORT = 65432  #camserver port

opcuaClient = Client("opc.tcp://" + HOST + ":3456/opcua/") #intialisiere opcua client

#deklaration von variablen
homeX, homeY, homeZ = 250, 0, 50    #Home-Koordinaten
ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ) #Kalibrierung des Arms auf die Home-Position
cubex = 25  #würfelgröße
redStack = 0    #Anzahl würfel auf rotem Ablagestapel
greenStack = 0  #Anzahl würfel auf grünem Ablagestapel
blueStack = 0   #Anzahl würfel auf blauem Ablagestapel
yellowStack = 0 #Anzahl würfel auf gelbem Ablagestapel
totalCubes = 5  #Anzahl der zu sortierenden Würfel
cubenum = 0     #Aktueller Würfel
pickupPos = [169.5,-145.8,-42]  #Koordinaten zum Aufheben des ersten Würfel
pickupXcorrection = 0.75        #Korrekturwerte zum Ausgleich von Abweichungen der Achsen
pickupYcorrection = 0.3         #Korrekturwerte zum Ausgleich von Abweichungen der Achsen
camPos = [135,-182,50]  #Koordinaten zur Farbermittlung vor der Kamera
Xdrop = 261             #X-Achse der Ablagestapel 
Yred = -143             #Y-Position des roten Stapels
Yblue = -52             #Y-Position des blauen Stapels
Ygreen = 42             #Y-Position des grünen Stapels
Yyellow = 134           #Y-Position des gelben Stapels

try:
    #verbinden zum opcua Server
    opcuaClient.connect()
    root = opcuaClient.get_root_node()
    temp = root.get_child(["0:Objects", "2:Raspi", "2:Temperatursensor", "2:DH22"])
    luefter = root.get_child(["0:Objects", "2:Raspi", "2:Luefter", "2:Luefter1"])

    #verbinden der Socket connection zum übertragen der Kameradaten
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, CAMPORT))

        #Schleife zum sortieren mehrerer würfel
        while cubenum < totalCubes:        
            #starten der Zeitmessung für Datenbankeintrag
            timestamp = calendar.timegm(time.gmtime())         

            #aufheben des aktuellen Würfels  
            ctrlBot.moveArmXYZ(pickupPos[0] + (pickupXcorrection*cubenum),pickupPos[1] + ((cubex+pickupYcorrection) * cubenum),pickupPos[2]+cubex)
            ctrlBot.moveArmXYZ(pickupPos[0] + (pickupXcorrection*cubenum),pickupPos[1] + ((cubex+pickupYcorrection) * cubenum),pickupPos[2])
            ctrlBot.toggleSuction()
            ctrlBot.moveArmXYZ(pickupPos[0] + (pickupXcorrection*cubenum),pickupPos[1] + ((cubex+pickupYcorrection) * cubenum),pickupPos[2]+2)
            if cubenum == 0:
                ctrlBot.moveArmXYZ(pickupPos[0] + (pickupXcorrection*cubenum),pickupPos[1] + ((cubex+pickupYcorrection) * cubenum) +1,pickupPos[2]+2)
                ctrlBot.moveArmXYZ(pickupPos[0] + (pickupXcorrection*cubenum),pickupPos[1] + ((cubex+pickupYcorrection) * cubenum) ,pickupPos[2]+2)
            else:
                ctrlBot.moveArmXYZ(pickupPos[0] + (pickupXcorrection*cubenum),pickupPos[1] + ((cubex+pickupYcorrection) * cubenum) -1,pickupPos[2]+2)
            ctrlBot.moveArmXYZ(pickupPos[0] + (pickupXcorrection*cubenum),pickupPos[1] + ((cubex+pickupYcorrection) * cubenum),camPos[2])
            ctrlBot.moveArmXYZ(pickupPos[0],camPos[1],camPos[2])
            ctrlBot.moveArmXYZ(camPos[0],camPos[1],camPos[2])
            
            #abrufen der Kamera- und Sensordaten in einer Schleife bis ein gültiger Farbwert empfangen wurde
            hasData = False
            while hasData == False:            
                s.sendall(b"get")   
                mytempval = temp.get_value()
                print("tempval is: ", mytempval)            
                data = s.recv(1024) 
                if data != b"error":
                    hasData = True
                else:
                    time.sleep(1) 
            

            #Auswertung der Kameradaten
            if data == b'Red':
                drop = nextDrop(redStack,Xdrop,Yred,pickupPos[2],cubex)
                redStack += 1
                luefter.set_value(25)
            elif data == b'Green':
                drop = nextDrop(greenStack,Xdrop,Ygreen,pickupPos[2],cubex)
                greenStack += 1
                luefter.set_value(50)
            elif data == b'Blue':
                drop = nextDrop(blueStack,Xdrop,Yblue,pickupPos[2],cubex)
                blueStack += 1
                luefter.set_value(75)
            elif data == b'Yellow':
                drop = nextDrop(yellowStack,Xdrop,Yyellow,pickupPos[2],cubex)
                yellowStack += 1
                luefter.set_value(100)
                

            print(f"Received {data!r}")
            print(f"{drop!r}")
            
            #ablegen des Würfels auf den erkannten Farbstapel
            ctrlBot.moveArmXYZ(pickupPos[0],camPos[1],camPos[2])
            ctrlBot.moveArmXYZ(pickupPos[0],drop[1],drop[2]+camPos[2])
            ctrlBot.moveArmXYZ(drop[0],drop[1],drop[2]+camPos[2])
            ctrlBot.moveArmXYZ(drop[0],drop[1],drop[2])
            ctrlBot.toggleSuction()
            ctrlBot.moveArmXYZ(drop[0],drop[1],drop[2]+camPos[2])
            ctrlBot.moveArmXYZ(pickupPos[0],drop[1],drop[2]+camPos[2])
            


            try:
                color =  data
                temperature = mytempval
                humidity = 0
                end_timestamp = calendar.timegm(time.gmtime())
                duration = abs(int((datetime.fromtimestamp(timestamp) - datetime.fromtimestamp(end_timestamp)).total_seconds()))
                costs = 0
                # generieren der nächsten id durch abruf des letzten id eintrages
                id = mongomaster.get_next_id()
                # erstellen eines Datenbankobjektes und einfügen in die Datenbank
                scan = Scan(id, timestamp, color, temperature, humidity, duration, costs) #id prüfen
                mongomaster.add_scan(scan)
            except:
                print("db error")
            
            #Nächster Würfel
            cubenum += 1
finally:
    #Trennen von opcua-server
    opcuaClient.disconnect()

    #Arm auf home Position fahren
    ctrlBot.moveArmXYZ(homeX, homeY, homeZ)