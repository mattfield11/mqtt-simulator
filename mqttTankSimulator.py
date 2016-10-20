#the code may be modified and reused but you should leave intact this header and the credits intact
#Matthew Field, www.smart-factory.net

#this simulates a level sensor on a tank and publishes the level to mosquitto mqtt server
#the level is determined by parameters fillRate and emptyRate which are read from mqtt server
#if fillRate and emptyRate are not received, the tank will fill and empty according to defaults
#the code may be modified and reused but you should leave intact this header and the credits intact
#Matthew Field, www.smart-factory.net


import paho.mqtt.client as mqtt
#threading is needed for timer function
import threading
#adjust the default variables below to suit you
mqttServer="192.168.1.10"
mqttPort="1883"
fillRate=11
emptyRate=10
level=0
valve=1
maximum= 10000
minimum= 1000
intervalPeriod=0.1


#every x seconds recalculate and send level data
def calculateLevel():
  global level
  global intervalPeriod
  global valve
  threading.Timer(intervalPeriod, calculateLevel).start()
  print "Level"
  level=level+(valve*fillRate)-emptyRate
  print (level)
  if level> maximum:
    valve=0
  elif level<minimum:
    valve=1
  if level<0:
    level=0
  print (level)
  client.publish("tankOut/1/level",payload=level, qos=0, retain=False)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #subscribe to all tank messages
    
    client.subscribe("tank/+/fillRate")
    


# The callback for when a fillrate message is received from the server.
def on_message_fillRate(client, userdata, msg):
    print ("fillratefunction")
    global fillRate
    fillRate= int(msg.payload)
    


client = mqtt.Client()
client.on_connect = on_connect
#the following line is not necessary but indicates syntax to use if we need
#to have different callbacks according to different messages received
#client.message_callback_add("#/#/fillRate", on_message_fillRate)
client.on_message = on_message_fillRate
client.connect(mqttServer,mqttPort, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#call calculateLevel function

calculateLevel()

client.loop_forever()
