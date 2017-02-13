## CONNECT TO WIFI
# Docs: https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_basics.html
import network
from umqtt.simple import MQTTClient
import machine
from machine import Pin, I2C

def do_connect(essid, password):
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print('connecting to network...')
		sta_if.active(True)
		sta_if.connect(essid, password)
		while not sta_if.isconnected(): 
			pass # Loop until we connect     


def concatBytes(msb, lsb):
	return int((msb << 8) + lsb)

def twos_comp(val, numBits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (numBits - 1))) != 0: 	# if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << numBits)        	# compute negative value
    return val                         		# return positive value as is

def processRaw(data):
	# Concatenate MSB with LSB
	x = concatBytes(data[0],data[1]) 
	y = concatBytes(data[2],data[3]) 
	z = concatBytes(data[4],data[5]) 
	# Convert from 2's complement binary to decimal integers
	x = twos_comp( x, 16 ) 
	y = twos_comp( y, 16 )
	z = twos_comp( z, 16 )
	return x,y,z

def buttonCallback(p):
	global calibrationOn
	calibrationOn = True
	print("Pin change", p)

## Connect to wifi
wifi_essid = "EEERover"
wifi_password = "exhibition"
do_connect(wifi_essid, wifi_password)

## Send message to broker
broker_addr = '192.168.0.10'
# broker_addr = '129.31.230.192'
client = MQTTClient(machine.unique_id(), broker_addr)
client.connect()
client.publish(b"esys/FourMusketeers", bytes('HELLO','utf-8'))


## Initialize button
buttonPin = Pin(0, Pin.IN)
buttonPin.irq(trigger=Pin.IRQ_FALLING, handler=buttonCallback)

## Calibration setup
angleDiff180 = 0
calibrationOn = False
doorIsOpen = False # Two states: True for Door Open, False for Door Closed

## I2C Comms
i2c_1 = I2C(scl=Pin(12), sda=Pin(13), freq=100000)
i2c_2 = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
addr1 = (i2c_1.scan())[0]
addr2 = (i2c_2.scan())[0]
# print(addr)

## Configuration Registers 
configRegA = 0
configRegB = 1
modeReg = 2
dataReg = 3
# Set to continuous read mode
i2c_1.writeto_mem(addr1, modeReg, b'\x00')
i2c_2.writeto_mem(addr2, modeReg, b'\x00')
# Set gain to minimum to avoid overflow
i2c_1.writeto_mem(addr1, configRegB, b'\xe0')
i2c_2.writeto_mem(addr2, configRegB, b'\xe0')
# Set default freq 15Hz
i2c_1.writeto_mem(addr1, configRegA, b'\x10')
i2c_2.writeto_mem(addr2, configRegA, b'\x10')
print("Finished configuration")

## Continuously read sensor data
while (True):
	## Read sensor data
	data1 = i2c_1.readfrom_mem(addr1, dataReg, 6) # Read 6 bytes from dataReg
	data2 = i2c_2.readfrom_mem(addr2, dataReg, 6) # Read 6 bytes from dataReg

	## Convert bytes into decimal values
	x1,y1,z1 = processRaw(data1)
	x2,y2,z2 = processRaw(data2)

	## Get useful differential sensor readings
	diff = (x1-x2, y1-y2, z1-z2)
	sumDiff = sum(diff)
	angleValueWithCalibration = sumDiff - angleDiff180

	## Check for change in door state
	if (angleValueWithCalibration > 100 and doorIsOpen==False) :
		doorIsOpen = True
		print("Door opened!")
		client.publish(b"esys/FourMusketeers", bytes("Door opened!",'utf-8'))
	elif (angleValueWithCalibration < 100 and doorIsOpen==True) :
		doorIsOpen = False
		print("Door closed!")
		client.publish(b"esys/FourMusketeers", bytes("Door closed!",'utf-8'))

	## Calibrate reading for sensors at 180 degree position
	if (calibrationOn == True): 
		angleDiff180 = sumDiff
		print("Calibrating 180 degrees at %s" %angleDiff180)
		calibrationOn = False

	# print(angleValueWithCalibration)
	# message = ("%s %s %s" %(diff[0],diff[1],diff[2]))
	# client.publish(b"esys/FourMusketeers", bytes(message,'utf-8'))