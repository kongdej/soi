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

# Arduino Serial port
ser = serial.Serial('/dev/ttyACM0',9600)

# NETPIE appid and apikeys
appid = "PudzaSOI"
gearkey = "xXCgD7V2IbWlArR"
gearsecret =  "QgrhkLHJ3xbbm58B9TsVtK15d"

microgear.create(gearkey,gearsecret,appid,{'debugmode': False})

def connection():
  print "Now I am connected with netpie"

def subscription(topic,message):
  print topic+"="+message
  if topic == "/PudzaSOI/cmd" :
      if message[1] == "1":
        rset = True
      else:
        rset = False
      GPIO.output(relays[int(message[0])], rset)
    
def disconnect():
  print "disconnect is work"

microgear.setalias("uno")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/msg");
microgear.subscribe("/cmd");
microgear.connect(False)

while True:
  y,m,d,h,mi,s,wd,wy,isd = time.localtime() 

  msg = ser.readline()  
  datalist = msg.split(',')
  if len(datalist) == 4:
    temp = datalist[0]
    ec   = datalist[1]
    tub  = datalist[2]
    ph   = datalist[3].rstrip()
    data = {"temp":temp, "ec":ec, "tub":tub, "ph":ph}
    microgear.writeFeed("SOIFeed",data)
  
  microgear.publish("/msg",msg)
  time.sleep(1)  
