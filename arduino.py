
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
         print "Calibrate"+message
#         ser.close()
#         ser.open()
         ser.write(message+"\r\n")	
#        rset = True
#      else:
#        rset = False
#      GPIO.output(relays[int(message[0])], rset)
    
def disconnect():
  print "disconnect is work"

microgear.setalias("uno")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/temp");
microgear.subscribe("/ec");
microgear.subscribe("/tub");
microgear.subscribe("/ph");
microgear.subscribe("/cmd");
microgear.subscribe("/eccalmsg");
microgear.connect(False)

while True:
  y,m,d,h,mi,s,wd,wy,isd = time.localtime() 

  msg = ser.readline()  
  datalist = msg.split(',')
#  print msg
  if len(datalist) == 4:
    temp = datalist[0]
    ec   = datalist[1]
    x  = datalist[2]
    ph   = datalist[3].rstrip()

    X = float(x) 
    tub = -1120.4*X*X + 5742.3*X - 4352.9
    if tub < 0:
      tub = 0

    data = {"temp":temp, "ec":ec, "tub":tub, "ph":ph}
    microgear.writeFeed("SOIFeed",data)
    microgear.publish("/temp", temp)
    microgear.publish("/ec", ec)
    microgear.publish("/tub", "%.2f" % tub)
    microgear.publish("/ph", ph)
  else:
    microgear.publish("/eccalmsg",msg)
  time.sleep(3)  
