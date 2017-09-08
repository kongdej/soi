
#!/usr/bin/python
import time
import serial

# Arduino Serial port
ser = serial.Serial('/dev/ttyACM0',9600)

while True:
  msg = ser.readline()
  datalist = msg.split(',')
  temp = datalist[0]
  ec   = datalist[1]
  x  = datalist[2]
  ph   = datalist[3].rstrip()

  X = float(x)
  tub = -1120.4*X*X + 5742.3*X - 4352.9
  datastr = temp+','+ec+','+"%.2f" % X+','+ph
  print datastr

  time.sleep(2)
