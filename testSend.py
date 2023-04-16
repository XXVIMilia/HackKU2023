import numpy as np
import cv2
import vpi
from PIL import Image
from serial import Serial
import time


ser = Serial("/dev/ttyUSB1", 115200)
    
        
i=0

while i < 10:    
    sendX = int(1).to_bytes(2, 'little')
    sendY = int(1).to_bytes(2, 'little')
    ser.write(sendX)
    ser.flush()
    ser.write(sendY)
    ser.flush()        
    sendX = int(200).to_bytes(2, 'little')
    sendY = int(400).to_bytes(2, 'little')
    ser.write(sendX)
    ser.flush()
    ser.write(sendY)
    ser.flush()
    sendX = int(400).to_bytes(2, 'little')
    sendY = int(400).to_bytes(2, 'little')
    ser.write(sendX)
    ser.flush()
    ser.write(sendY)
    ser.flush()
    sendX = int(400).to_bytes(2, 'little')
    sendY = int(200).to_bytes(2, 'little')  
    ser.write(sendX)
    ser.flush()
    ser.write(sendY)
    ser.flush()
    time.sleep(0.1)
    i=i+1
ser.write(('\n').encode())
# ser.write(('\n').encode())
ser.flush()
# print(int("65535").to_bytes(2, 'little'))
# ser.write(int("65535").to_bytes(2, 'little'))
# ser.flush()
# ser.write(int("65535").to_bytes(2, 'little'))
# ser.flush()
# ser.write(int("65535").to_bytes(2, 'little'))
        
        