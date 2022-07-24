import cv2 as cv
import mediapipe as mp
import numpy as np
import time

"""ARDUINO PART"""
import serial   #PySerial
#arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)    #Ini untuk ESP32
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
 
cap = cv.VideoCapture(1)    #Kamera
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

cTime = pTime = 0

mpFaceDetection = mp.solutions.face_detection
#mpDraw = mp.solutions.drawing_utils 
faceDetection = mpFaceDetection.FaceDetection(0.70) #Default confidence oriignal = 50%

while True:
    succes, img = cap.read()
    img = cv.flip(img,1)
    h, w, c = img.shape

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:  #Jika ada terdeteksi
        #print(f'Jumlah Wajah: {len(results.detections)}')    #check num of face, you can play with it
        for id, detection in enumerate(results.detections):
            if(id == 0):    #Only follow 1 face (the face with the most high percentage)
                #print(detection.location_data.relative_bounding_box)    #Check the output of detecion
                bboxC = detection.location_data.relative_bounding_box               
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)    #Nyesuain sama ukuran ghambar biar koordinatnya segambar juga
                cv.rectangle(img, bbox, (255,0,255), 2) #Draw boundingbox with OpenCv
                #cv.putText(img, f'{int(detection.score[0] * 100)} %', (bbox[0], bbox[1] - 10), cv.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

                #sending coordinates to Arduino
                X = (bbox[0]+(bbox[2]//2))
                X = np.interp(X,[0,w],[35,94])  #Mapping maks right and left of the lcd screen - it's depending off your camrea wide angle
                Y = (bbox[1]+(bbox[3]//2))
                Y = np.interp(Y,[0,h],[22,42])  #mapping 
                string='X{}Y{}'.format(int(X),int(Y))
                print(string)
                arduino.write(string.encode('utf-8'))     
                time.sleep(0.08)  

    #plot the squared region in the center of the screen
    cv.rectangle(img,(640//2-40,480//2-40), (640//2+40,480//2+40), (255,255,255),3)

    #Show image video
    cv.imshow("Webcam",img)

    if cv.waitKey(20) & 0xFF==ord('d'): #press 'd' button to break looping 
        break

cap.release()
cv.destroyAllWindows()  #Clode window when finish