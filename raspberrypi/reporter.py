#!/usr/bin/python

import microgear.client as microgear
import time
import requests

appid = "PudzaSOI"
gearkey = "J5eQimLa7t19HfG"
gearsecret =  "zn89Ok8po5dFyMKi5Pb3A3zgW"

# Thingspeak
urlThingspeak = "https://api.thingspeak.com/update.json"
api_key = "58BCA689FPZ7PMZG"

temp="0"
ec="0"
tub="0"
ph="0"

microgear.create(gearkey,gearsecret,appid,{'debugmode': False})

def connection():
  print "Now I am connected with netpie"

def subscription(topic,message):
  global temp,ec,tub,ph

#  print topic+" "+message

  if topic == "/PudzaSOI/temp" :
    temp= message;
  if topic == "/PudzaSOI/ec" :
    ec = message
  if topic == "/PudzaSOI/tub" :
    tub = message
  if topic == "/PudzaSOI/ph" :
    ph = message

def disconnect():
  print "disconnect is work"

microgear.setalias("reporter")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/temp")
microgear.subscribe("/ec");
microgear.subscribe("/tub");
microgear.subscribe("/ph");

microgear.connect(False)

while True:
  y,m,d,h,mi,s,wd,wy,isd = time.localtime() 

  if s % 15 == 0:
    payload = {'api_key': api_key, 'field1' : temp,'field2' : ec,'field3' : tub,'field4' : ph}
    r = requests.post(urlThingspeak,params=payload,verify=False)
#    print payload

  time.sleep(1)
