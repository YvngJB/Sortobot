from opcua import ua, uamethod, Server
from opcua.ua import ObjectIds
import netifaces as ni
import RPi.GPIO as GPIO
from random import randint
import board
import time
import datetime
import adafruit_dht

class Opcuaserver:
    def __init__(self) -> None:
        self.server = Server()
        #self.IPV4_Address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        self.url = "opc.tcp://192.168.187.2:3456/opcua/"
        #self.url = "opc.tcp://10.62.255.2:3456/opcua/"
        self.server.set_endpoint(self.url)

        self.server.set_security_policy(
            [
                ua.SecurityPolicyType.NoSecurity
            ])

        # OPCUA Namensraum festlegen
        self.name = "OPCUA_Musterplatine"
        self.addspace = self.server.register_namespace(self.name)
        self.node = self.server.get_objects_node()
        self.Raspi = self.node.add_object(self.addspace, "Raspi")
        # Ordner für das Objekt Raspi anlegen
        self.myfolder = self.Raspi.add_folder(self.addspace, "Temperatursensor")
        self.myfolder2 = self.Raspi.add_folder(self.addspace, "Luefter")
        # OPUA Datenpnkte "TempSensor1" festlegen
        self.Sensor1 = self.myfolder.add_variable(self.addspace, "DH22", 20.1)
        self.Luefter1 = self.myfolder2.add_variable(self.addspace, "Luefter1", 20)
        self.Time = self.node.add_variable(self.addspace, "Time", 0)

        self.Luefter1.set_writable()

        # OPCUA-Server starten
        self.server.start()
        print("Server startet auf {}".format(self.url))

        # GPIOs konfigurieren
        self.sensorPIN = 4
        self.luefterPIN = 13
        self.ledPIN = 23

        # Zählweise der Pins festlegen
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # GPIO Eingänge festlegen
        GPIO.setup(self.sensorPIN, GPIO.IN)

        # GPIO Ausgänge festlegen
        GPIO.setup(self.luefterPIN, GPIO.OUT)
        GPIO.setup(self.ledPIN, GPIO.OUT)

        # alles ausschalten
        GPIO.output(self.luefterPIN, GPIO.LOW)
        GPIO.output(self.ledPIN, GPIO.LOW)

        self.pwm1 = GPIO.PWM(self.luefterPIN, 100)
        self.pwm1.start(100.0)

        print("!!! Lesen des Sensors !!!")

        # Device für Sensor
        # Initial the dht device, with data pin connected to:
        self.dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        self.temperature_c = 0
        self.humidity = 0

    def setFanDuty(self, sfdc=0.0):  # Setzt den Dutycycle (in % von 0.0-100.0) für den Lüfter
         self.pwm1.ChangeDutyCycle(sfdc)
        
    def run(self):
        while True:
            # Zeit ermitteln
            TIME = datetime.datetime.now()

            self.setFanDuty(self.Luefter1.get_value())
            
            # Temperatur messen
            try:
                # Print the values to Console
                self.temperature_c = self.dhtDevice.temperature
                self.humidity = self.dhtDevice.humidity
                self.Sensor1.set_value(self.temperature_c)
                print(
                    "Temp: {:.1f} C    Humidity: {}%  Zeit:{:s}".format(
                         self.temperature_c, self.humidity, TIME.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                    )
                )
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                self.dhtDevice.exit()
                raise error

            time.sleep(2)

if __name__ == "__main__":
    server = opcuaserver()
    server.run()