from paho.mqtt import client as mqtt_client
import random

class MQTTClient:
    _config = {
        'broker' : 'localhost',
        'port' : 1883,
        'topic' : 'python/mqttclient'
    }
    _broker = None
    _port = None
    _topic = None
    _client_id = None
    _client = None
    def __init__(self) -> None:
        self._broker = self._config['broker']
        self._port = self._config['port']
        self._topic = self._config['topic']
        self._client_id = f'python-mqttclient-{random.randint(0, 1000)}'
        pass
    def loadConfig(self, config) -> None:
        if 'broker' in config and 'port' in config and 'topic' in config:
            self._config = config
            self.__init__()
        else:
            print("[Error] : New Config could not be loaded. Missing Parameter. Default config is used.")
        pass
    def connect(self) -> None:
        self._connect_mqtt()
        pass
    def _connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        self._client = mqtt_client.Client(self._client_id)
        #self._client.username_pw_set(username, password)
        self._client.on_connect = on_connect
        try:
            self._client.connect(self._broker, self._port)
        except:
            print("[Error] : Could not connect to broker. Please try again.")
            exit()
        return self._client
    def publish(self, message):
        result = self._client.publish(self._topic, message)
        status = result[0]
        if status == 0:
            print("[Success] : Data send to broker.")
        else:
            print("[Error] : Failed to send message.")
    def subscribe(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        self._client.subscribe(self._topic)
        self._client.on_message = on_message

        self._client.loop_forever()
        