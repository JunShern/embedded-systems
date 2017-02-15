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
    global msgList
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

    ## Update msgList for log of messages
    msgList.append(msgObject)
    while (len(msgList)>5): msgList.pop(0)

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
    lineIndex = 0
    for msgObj in msgList:
        ## Create log string
        textString = msgObj['timeString']
        if (msgObj['doorState'] == 1):
            textString = textString + " : Door opened."
        elif (msgObj['doorState'] == 0):
            textString = textString + " : Door closed."
        else:
            textString = textString + " : There's something strange, in the neighborhood."
        ## Draw log string
        text = pFont.render(textString, 1, (255,255,255))
        w,h = pFont.size(textString)
        screen.blit(text, (10, height - (2*h)*(1+lineIndex)) )

        lineIndex += 1
    return

pygame.init()

## Global variables
doorState = 0
msgList = list()
pFont = pygame.font.SysFont("monospace", 16)
## Graphics / UI
width = 500
height = 700
size = (width, height)
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
