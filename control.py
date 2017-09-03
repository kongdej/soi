#!/usr/bin/python
import microgear.client as microgear
import time
import serial
import RPi.GPIO as GPIO

# Raspery GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
relays = [29,31,33,35,37,36,38,40]

for i in range(0,8) :
  GPIO.setup(relays[i], GPIO.OUT)
  GPIO.output(relays[i], False)

# NETPIE appid and apikeys
appid = "PudzaSOI"
gearkey = "NPzmYKy02sD4Gw8"
gearsecret =  "9rSJOGLWDH8Ct2C8bnQh6b96S"

microgear.create(gearkey,gearsecret,appid,{'debugmode': False})

def connection():
  print "Now I am connected with netpie"

def subscription(topic,message):
  print topic+"="+message
  if topic == "/PudzaSOI/data" :
    datalist = message.split(',')
    ph = float(datalist[3].rstrip())
    if ph > 9 :
      print 'co2 on ph=' + str(ph)
      GPIO.output(relays[2], 1)
    if ph < 8:
      print 'co2 off ph=' + str(ph)
      GPIO.output(relays[2], 0)

def disconnect():
  print "disconnect is work"

microgear.setalias("control")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/data");

microgear.connect(False)
while True:
  pass
