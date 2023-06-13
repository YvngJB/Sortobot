from opcua import ua, uamethod, Server
from opcua.ua import ObjectIds
import netifaces as ni
import RPi.GPIO as GPIO
from random import randint
import board
import time
import datetime
import adafruit_dht

# UMBAUEN WIE CAM SERVER!   

class opcuaserver:
    def __init__(self) -> None:
        server = Server()
        #Get the ip address
        IPV4_Address = ni.ifaddresses('wlan0') [ni.AF_INET][0]['addr']
        url="opc.tcp://192.168.187.2:4840/opcua/"
        server.set_endpoint(url)

        server.set_security_policy(
            [
                ua.SecurityPolicyType.NoSecurity
            ])

        #OPCUA Namensraum festlegen
        name="OPCUA_Musterplatine"
        addspace=server.register_namespace(name)
        node=server.get_objects_node()
        Raspi=node.add_object(addspace,"Raspi")
        #Ordner für das Objekt Raspi anlegen
        myfolder = Raspi.add_folder(addspace, "Temperatursensor")
        myfolder2 = Raspi.add_folder(addspace, "Luefter")
        #OPUA Datenpnkte "TempSensor1" festlegen
        Sensor1 = myfolder.add_variable(addspace,"DH22",20.1)
        Luefter1 = myfolder2.add_variable(addspace,"Luefter1",20)
        Time = node.add_variable(addspace,"Time",0)

        Luefter1.set_writable()

        #OPCUA-Server starten
        server.start()
        print("Server startet auf {}",format(url))



        #GPIOs konfigurieren
        sensorPIN = 4
        luefterPIN = 13
        ledPIN = 23

        # Zählweise der Pins festlegen
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #GPIO Eingänge festlegen
        GPIO.setup(sensorPIN, GPIO.IN)

        #GPIO Ausgänge festlegen
        GPIO.setup(luefterPIN, GPIO.OUT)
        GPIO.setup(ledPIN, GPIO.OUT)

        # alles ausschalten
        GPIO.output(luefterPIN,GPIO.LOW)
        GPIO.output(ledPIN,GPIO.LOW)

        pwm1 = GPIO.PWM(luefterPIN, 100)
        pwm1.start(100.0)


        print ("!!! Lesen des Sensors !!!")

        # Device für Sensor
        # Initial the dht device, with data pin connected to:
        dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        temperature_c = 0
        humidity = 0
        print (pwm1)


    def setFanDuty(self, sfdc = 0.0): # Setzt den Dutycycle (in % von 0.0-100.0) für den Lüfter
        print ("!!! sfd !!!")
        print (pwm1)
        pwm1.ChangeDutyCycle(sfdc)
        print ("!!! sfd? !!!")   


    def run(self):
        while True:
            #Zeit ermitteln
            TIME = datetime.datetime.now()
            
            self.setFanDuty (Luefter1.get_value())
            #print(Luefter1.get_value())
            
            # Temperatur messen
            try:
                # Print the values to Console
                temperature_c = dhtDevice.temperature
                humitidy = dhtDevice.humidity
                Sensor1.set_value(temperature_c)
                print(
                    "Temp: {:.1f} C    Humidity: {}%  Zeit:{:s}".format(
                         temperature_c, humidity, TIME.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                    )
                )
                
                #if Luefter1.get_value() == 1 :
                 #   GPIO.output(luefterPIN,GPIO.HIGH)   
                 #   GPIO.output(ledPIN,GPIO.HIGH)
                    
                #else:
                  #  GPIO.output(luefterPIN,GPIO.LOW)
                  #  GPIO.output(ledPIN,GPIO.LOW)
                               
                #print(str(Luefter1.get_value()))    
               
                   # physikalischen Lüfter anschalten
                    #GPIO.output(luefterPIN,GPIO.HIGH)
                    ## LED anschalten	
                    #GPIO.output(ledPIN,GPIO.HIGH)
                    #break
                     
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error        
            
            time.sleep(2)   
     
        