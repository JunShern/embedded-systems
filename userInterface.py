import paho.mqtt.client as mqtt
import time

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("esys/FourMusketeers")

def on_message(client, userdata, msg):
    message = (msg.payload.decode())
    print(message)
    if (message == "OPEN"):
    	doorState = 1
    elif (message == "CLOSE"):
    	doorState = 0

global doorState 
doorState = 0
# client = mqtt.Client()
client = mqtt.Client("", True, None, mqtt.MQTTv31)

client.on_connect = on_connect
client.on_message = on_message

broker_addr = '192.168.0.10'
client.connect(broker_addr,1883,60)

client.loop_forever()
