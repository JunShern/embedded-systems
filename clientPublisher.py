import paho.mqtt.client as mqtt

# This is the Publisher

mqtt_client = mqtt.Client("", True, None, mqtt.MQTTv31)
client = mqtt.Client()

broker_addr = '192.168.0.10'
client.connect('localhost',1883,60)

client.publish("topic/test", "Hello world!")
client.disconnect()