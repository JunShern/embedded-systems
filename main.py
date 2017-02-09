## CONNECT TO WIFI
# Docs: https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_basics.html
import network

from umqtt.simple import MQTTClient
# import machine

# wifi_essid = "EEERover"
# wifi_password = "exhibition"

# def do_connect(essid, password):
# 	sta_if = network.WLAN(network.STA_IF)
# 	if not sta_if.isconnected():
# 		print('connecting to network...')
# 		sta_if.active(True)
# 		sta_if.connect(essid, password)
# 		while not sta_if.isconnected(): 
# 			pass # Loop until we connect     

# do_connect(wifi_essid, wifi_password)

# ## SEND MESSAGE TO SERVER
# broker_addr = '192.168.0.10'
# client = MQTTClient(machine.unique_id(), broker_addr)
# client.connect()
# client.publish(b"esys/FourMusketeers", bytes('HELLO','utf-8'))

def concatBytes(msb, lsb):
	return int((msb << 8) + lsb)

## I2C Comms
from machine import Pin, I2C
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
addr = (i2c.scan())[0]
print(addr)

## Configuration Registers 
configRegA = 0
configRegB = 1
modeReg = 2
dataReg = 3
# Set to continuous read mode
i2c.writeto_mem(addr, modeReg, b'\x00')
# Set gain to minimum to avoid overflow
i2c.writeto_mem(addr, configRegB, b'\xe0')
# Set minimum freq 0.75Hz
i2c.writeto_mem(addr, configRegA, b'\x00')
print("Finished configuration")
while (True):
	data = i2c.readfrom_mem(addr, dataReg, 6) # Read 6 bytes from dataReg
	x = concatBytes(data[0],data[1])
	y = concatBytes(data[2],data[3])
	z = concatBytes(data[4],data[5])
	print("%d %d %d" %(x,y,z))