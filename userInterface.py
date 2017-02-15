import paho.mqtt.client as mqtt
import time
import pygame
import ujson

class MessageObject(object):
    def __init__(self, textString):
        self.timeString = getTimeAsString()
        self.textString = textString

def getTimeAsString():
    # Returns time as DD/MM/YYYY - HH:MM:SS 
    t = time.localtime()
    timeString = ("%02d/%02d/%04d - %02d:%02d:%02d"
        %(t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec))
    return timeString

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("esys/FourMusketeers")

def on_message(client, userdata, msg):
    global doorState
    global msgList
    message = (msg.payload.decode())
    msgObject = ujson.loads(message)

    ## Special handler for doorState-related messages (Open or Close)
    if ('timeString' in msgObject and 'doorState' in msgObject):
        print(msgObject['timeString'])
        print(msgObject['doorState'])
        if (msgObject['doorState'] == '1'):
        	doorState = 1
        elif (msgObject['doorState'] == '0'):
        	doorState = 0
    
    ## Update msgList for log of messages
    msgList.append(msgObject)
    while (len(msgList)>8): msgList.pop(0)

    # Update graphics
    updateGraphics()

def updateGraphics():
    bgColor = pygame.Color(10,10,10) 
    screen.fill(bgColor)
    drawFloorPlan()
    drawDoorState(width-120, height/2-10, doorState)
    drawMessageLog()
    pygame.display.update()
    return

def drawFloorPlan():
    screen.blit(floorplanImg, (30,30)) 
    pygame.display.flip()
    return

def drawDoorState(xpos, ypos, doorOpen): #(xpos, ypos, doorState, doorInOut):
    print("Door state is %s" %(doorOpen))
    if doorOpen:
        pygame.draw.rect(screen,(0,0,200),[xpos,ypos,10,60])
    else:
        pygame.draw.rect(screen,(0,0,200),[xpos,ypos,60,10])
    return

# def drawDoor(xpos, ypos, doorState, doorInOut):
#     WHITE = (255, 255, 255)
#     BLUE = (0, 0, 255)
#     screen.fill(WHITE)
#     if not doorState:
#         #Add rotation code: help: http://stackoverflow.com/a/36512406/4748004
#     else:
#         pygame.draw.rect(screen, BLUE, (xpos, ypos, 100, 20))

def drawMessageLog():
    lineIndex = 0
    for msgObj in msgList:
        ## Create log string
        textString = msgObj['timeString']
        if ('doorState' in msgObj):
            if (msgObj['doorState'] == '1'):
                textString = textString + " : Door opened."
            elif (msgObj['doorState'] == '0'):
                textString = textString + " : Door closed."
            else:
                textString = textString + " : There's something strange, in the neighborhood."
        elif ('textString' in msgObj):
            textString = textString + " : " + msgObj['textString'] 
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
greetingMessage = {"textString":"Welcome to Home Security!", "timeString":getTimeAsString()}
msgList.append(greetingMessage)

pFont = pygame.font.SysFont("monospace", 16)
## Graphics / UI
width = 500
height = 700
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("IoT Home Security")
## Load image of floorplan
floorplanImg = pygame.image.load("floorplan.jpg")
floorplanImgRect = floorplanImg.get_rect()
updateGraphics()

## MQTT message subscriber
client = mqtt.Client()
client = mqtt.Client("", True, None, mqtt.MQTTv31)

client.on_connect = on_connect
client.on_message = on_message

broker_addr = '192.168.0.10'
# broker_addr = 'localhost'
client.connect(broker_addr,1883,60)

client.loop_forever()
