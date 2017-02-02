## CONNECT TO WIFI
# Docs: https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_basics.html
import network

from umqtt.simple import MQTTClient
import machine

wifi_essid = "EEERover"
wifi_password = "exhibition"

def do_connect(essid, password):
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print('connecting to network...')
		sta_if.active(True)
		sta_if.connect(essid, password)
		while not sta_if.isconnected(): 
			pass # Loop until we connect     

do_connect(wifi_essid, wifi_password)

## SEND MESSAGE TO SERVER
broker_addr = '192.168.0.10'
client = MQTTClient(machine.unique_id(), broker_addr)
client.connect()
client.publish(b"esys/FourMusketeers", bytes('HELLO','utf-8'))
