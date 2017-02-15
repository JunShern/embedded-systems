import paho.mqtt.client as mqtt
import time
import pygame
import ujson

class MessageObject(object):
    def __init__(self, doorState):
        self.timeString = getTimeAsString()
        self.doorState = doorState

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("esys/FourMusketeers")

def on_message(client, userdata, msg):
    global doorState
    message = (msg.payload.decode())
    msgObject = ujson.loads(message)
    try:
        print(msgObject['timeString'])
        print(msgObject['doorState'])
        if (msgObject['doorState'] == 1):
        	doorState = 1
        elif (msgObject['doorState'] == 0):
        	doorState = 0
    except ValueError:
        print("Expected JSON string with keys 'timeString' and 'doorState'")
    # Update graphics
    updateGraphics()

def updateGraphics():
    bgColor = pygame.Color(10,10,10) 
    screen.fill(bgColor)
    drawFloorPlan()
    drawDoorState(doorState)
    drawMessageLog()
    pygame.display.update()
    return

def drawFloorPlan():
    return

def drawDoorState(doorOpen):
    print("Door state is %s" %(doorOpen))
    if doorOpen:
        pygame.draw.rect(screen,(200,200,200),[20,20,250,30])
    else:
        pygame.draw.rect(screen,(200,200,200),[20,20,30,250])
    return

def drawMessageLog():
    return

## Global variables
doorState = 0

## Graphics / UI
pygame.init()
size = (500, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("IoT Home Security")
updateGraphics()

## MQTT message subscriber
client = mqtt.Client()
client = mqtt.Client("", True, None, mqtt.MQTTv31)

client.on_connect = on_connect
client.on_message = on_message

# broker_addr = '192.168.0.10'
broker_addr = 'localhost'
client.connect(broker_addr,1883,60)

client.loop_forever()
