import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.187.2" 
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("Publishing message to topic","FBS/aDamn/Luftfeuchtigkeit")
client.publish("FBS/aDamn/Luftfeuchtigkeit","OFF")