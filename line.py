#!/usr/bin/python

import microgear.client as microgear
import time
import requests
import datetime
import sys

appid = "PudzaSOI"
gearkey = "J5eQimLa7t19HfG"
gearsecret =  "zn89Ok8po5dFyMKi5Pb3A3zgW"

# Line notify
urlLine = "https://notify-api.line.me/api/notify"
LINE_ACCESS_TOKEN="u4NyjAypiCE6dn7IW0Xo6yZTCEbByPkw86jI3eZOzjT" 

temp="0"
ec="0"
tub="0"
ph="0"
i=0

microgear.create(gearkey,gearsecret,appid,{'debugmode': False})

def connection():
  print "Now I am connected with netpie"

def subscription(topic,message):
  global temp,ec,tub,ph,i

  print topic+" "+message

  if i >= 4:
    y,m,d,h,mi,s,wd,wy,isd = time.localtime() 
    textmsg = "\n"+str(datetime.datetime(y, m, d, h, mi, s))+"\n"    
    textmsg += "Temperature = "+ temp + " C\n"
    textmsg += "EC = "+ ec + " mS/cm\n"
    textmsg += "Turbidity = "+ tub + " mg/L\n"
    textmsg += "PH = "+ ph 
    msg = {"message":textmsg} 
    LINE_HEADERS = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":"Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    resp =session.post(urlLine, headers=LINE_HEADERS, data=msg)
    print(resp.text)
    sys.exit()

  if topic == "/PudzaSOI/temp" :
    i+=1
    temp= message
  if topic == "/PudzaSOI/ec" :
    i+=1
    ec = message
  if topic == "/PudzaSOI/tub" :
    i+=1
    tub = message
  if topic == "/PudzaSOI/ph" :
    i+=1
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
microgear.connect(True);
