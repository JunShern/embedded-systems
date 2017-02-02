# from umqtt.simple import MQTTClient
# import machine
# client = MQTTClient(machine.unique_id(), BROKER_ADDRESS)
# client.connect()
# client.publish("HELLO", bytes(data,'utf-8'))

## CONNECT TO WIFI
# Docs: https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_basics.html

import network
import socket

wifi_essid = "EEERover"
wifi_password = "exhibition"

def do_connect(essid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(essid, password)
        while not sta_if.isconnected():
            pass
    ## Declare victory
    if (sta_if.isconnected()):
		print("We are online!")
		print('network config:', sta_if.ifconfig())

do_connect(wifi_essid, wifi_password)

## CONNECT TO SOCKETS
# addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
# print(addr_info)
# addr = addr_info[0][-1]
# s = socket.socket()
# s.connect(addr)

# while True:
# 	data = s.recv(500)
# 	print(str(data, 'utf8'), end='')

# def http_get(url):
# 	_, _, host, path = url.split('/', 3)
# 	addr = socket.getaddrinfo(host, 80)[0][-1]
# 	s = socket.socket()
# 	s.connect(addr)
# 	s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' %(path,host), 'utf8'))
# 	while True:
# 		data = s.recv(100)
# 		if data: 
# 			print(str(data, 'utf8'), end='')
# 		else:
# 			break
# 	s.close()

# http_get('https://en.wikipedia.org/wiki/Suillus_salmonicolor')