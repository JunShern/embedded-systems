import paho.mqtt.client as mqtt
import time 
import ujson

class MessageObject(object):
	def __init__(self, doorState):
		self.timeString = getTimeAsString()
		self.doorState = doorState

def getTimeAsString():
	# Returns time as DD/MM/YYYY - HH:MM:SS 
	t = time.localtime()
	timeString = ("%02d/%02d/%04d - %02d:%02d:%02d"
		%(t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec))
	return timeString

def sendOpen():
	doorState = 1
	msg = MessageObject(doorState)
	client.publish("esys/FourMusketeers", ujson.dumps(msg))

def sendClose():
	doorState = 0
	msg = MessageObject(doorState)
	client.publish("esys/FourMusketeers", ujson.dumps(msg))

# This is the Publisher
mqtt_client = mqtt.Client("", True, None, mqtt.MQTTv31)
client = mqtt.Client()

# broker_addr = '192.168.0.10'
broker_addr = 'localhost'
client.connect(broker_addr,1883,60)

client.publish("esys/FourMusketeers", "OPEN")
client.publish("esys/FourMusketeers", "CLOSE")
# client.disconnect()