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

microgear.create(gearkey,gearsecret,appid,{'debugmode': False})

def connection():
  print "Now I am connected with netpie"

def subscription(topic,message):
  print topic+" "+message

  if topic == "/PudzaSOI/data" :
    y,m,d,h,mi,s,wd,wy,isd = time.localtime() 
    temp,ec,tub,ph = message.split(',');
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

def disconnect():
  print "disconnect is work"

microgear.setalias("reporter")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/data");
microgear.connect(True);
