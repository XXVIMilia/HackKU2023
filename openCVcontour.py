import numpy as np
import cv2
import vpi
from PIL import Image
from serial import Serial
import time


#ser = Serial("/dev/ttyUSB0", 9600)



def gstreamer_pipeline(
    sensor_id=0,
    capture_width=3280,
    capture_height=2464,
    display_width=960,
    display_height=720,
    framerate=10,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
# removes smaller contours, i.e. removes noise from image
def highpass(contour):
    if len(contour) > 450:
        return (True)
    return (False)

def show_camera():
    backend = vpi.Backend.CUDA


    window_title = "CSI Camera"
    left_capture = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0,flip_method=2), cv2.CAP_GSTREAMER)

    if left_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            for i in range(2):
                ret_valL, frameL = left_capture.read()
            
            stream_Left = vpi.Stream()
            
            imgray = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
            img_blurgray = cv2.GaussianBlur(imgray, (9,9), 0)
            (thresh, blackAndWhiteImage) = cv2.threshold(img_blurgray, 75, 255, cv2.THRESH_BINARY)
            #cv2.imshow('Black white image', blackAndWhiteImage)
            img_blur = cv2.GaussianBlur(blackAndWhiteImage, (9,9), 0)
            edged = cv2.Canny(img_blur, 100, 125)
            #cv2.waitKey(0)
            contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)
            
            cv2.imshow('Canny Edges After Contouring', edged)
            cv2.waitKey(0)
            
            print("Number of Contours found = " + str(len(contours)))
            
           
            sum=0
            print(len(contours))

            result = list(filter(highpass,contours))
            result.pop(0)
            result.pop(-1)
            print("after poping: " + str(len(result)))
            # print(len(result[0]))
            cv2.drawContours(frameL, result, -1, (0, 255, 0), 3)
            cv2.imshow('Contours', frameL)
            cv2.waitKey(0)
            return(result)
            while True:
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frameL)
                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            left_capture.release()
            cv2.destroyAllWindows()
    
if __name__ == "__main__":
    toESP = show_camera()

    print("sending data NOWWWWWWWWWWWWWWWWWWWWWWWWWWw")
    ser = Serial("/dev/ttyUSB1", 115200)
    for arra in toESP:
        i=0
        print(type(arra.tolist()))
        newArr = arra.tolist()
        print("another contourrrrrrrrrr")
        
        while i<len(newArr)-1:
            
            i = i+1
            print(str(newArr[i][0][0]))
            x = str(newArr[i][0][0])
            x=x.strip()
            y= str(newArr[i][0][1])
            y=y.strip()

            sendX = int(x).to_bytes(2, 'little')
            
            sendY = int(y).to_bytes(2, 'little')
            # print(sendX)
            # print("-----")
            # print(newArr[i][0][1])
            # print(sendY)
            ser.write(sendX)
            ser.flush()
            ser.write(sendY)
            ser.flush()
            # time.sleep(0.5)
        
        ser.write(('\n').encode())
        ser.flush()
        ser.write(('\n').encode())
        ser.flush()
        time.sleep(1.5)
  
     

