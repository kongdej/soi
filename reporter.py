#!/usr/bin/python

import microgear.client as microgear
import time
import requests
import datetime

appid = "PudzaSOI"
gearkey = "J5eQimLa7t19HfG"
gearsecret =  "zn89Ok8po5dFyMKi5Pb3A3zgW"

# Thingspeak
urlThingspeak = "https://api.thingspeak.com/update.json"
api_key = "58BCA689FPZ7PMZG"

microgear.create(gearkey,gearsecret,appid,{'debugmode': False})

def connection():
  print "Now I am connected with netpie"

def subscription(topic,message):
#  print topic+" "+message
  if topic == "/PudzaSOI/data" :
    y,m,d,h,mi,s,wd,wy,isd = time.localtime() 
    temp,ec,tub,ph = message.split(',');
    payload = {'api_key': api_key, 'field1' : temp,'field2' : ec,'field3' : tub,'field4' : ph}
    r = requests.post(urlThingspeak,params=payload,verify=False)
    print payload

def disconnect():
  print "disconnect is work"

microgear.setalias("reporter")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/data");
microgear.connect(True)
