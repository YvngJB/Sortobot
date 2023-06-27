
from client import MQTTClient
import time
import datetime
import json
from scan import Scan
from controller import Controller

mqtt = MQTTClient()

config = {
    'broker' : 'localhost',
    'port' : 1883,
    'topic' : '/robby/mqtt'
}
mqtt.loadConfig(config)
mqtt.connect()


db = Controller("mongodb://10.100.20.101")
db.switch_database("robby")
db.switch_collection("scans")

temp = db.get_products()

data = {
    'scans' : temp
}

data = json.dumps(data)

while True:
    try:
        temp = db.get_products()
        data = {
            'scans' : temp
        }
        data = json.dumps(data)
 
        mqtt.publish(data)
        time.sleep(1)
    except KeyboardInterrupt:
        print("Bye")
        exit()
