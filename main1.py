from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from motor_driver import Motor
import RPi.GPIO as GPIO
from time import sleep
from ultrasonic import *

motor = Motor(17,22,27,2,3,4)

app = Flask(__name__, template_folder='./templates')
camera = cv2.VideoCapture(0)

global capture, rec, out, rec_frame
capture = 0
rec = 0
switch = 1

try:
    os.mkdir('./shots')
except OSError as error:
    pass

try:
    os.mkdir('./videos')
except OSError as error:
    pass


#############################################################
classNames = []
classFiles = 'coco.names'
with open(classFiles,'rt') as f:
    classNames = f.read().strip('\n').split('\n')
    

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img,draw=True, nms=0.5,threshold=0.45,objects=[]):
    global className
    classIds, confs, bbox  = net.detect(img,nmsThreshold=nms,confThreshold=threshold)
    if len(objects) == 0:
        objects = classNames
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(),bbox):
            className = classNames[classId-1]
            if className in objects:
                if (draw):
                    objectInfo.append([box, className])
                    cv2.rectangle(img,box,color=(0,255,255),thickness=1)
                    cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    #cv2.putText(img,str(round(confidence*100,2)),(box[0]+90,box[1]+30),
                                 #cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo


def record(out):
    global rec_frame
    while rec:
        time.sleep(0.05)
        out.write(rec_frame)

def gen_frames():
    global out, capture, rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            result,objects = getObjects(frame,draw=True,nms=0.6,threshold=0.45,objects=['car','bird','cell phone','person','eye glasses','book'])    


            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(result,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

@app.route('/')
def index():
    return render_template('sneha.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch, camera, capture, rec, out
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            capture = 1
        elif request.form.get('rec') == 'Start/Stop Recording':
            rec = not rec
            if rec:
                now=datetime.datetime.now()
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                filename = os.path.sep.join(['videos', "vid_{}.avi".format(str(now).replace(":",''))])
                out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
                # Start new thread for recording the video
                thread = Thread(target=record, args=[out,])
                thread.start()
            elif not rec and out is not None:
                out.release()
                out = None
    elif request.method == 'GET':
        return render_template('sneha.html')
    return render_template('sneha.html')
@app.route('/left_side')

def left_side():

    print ("LEFT")
    motor.move(0.6,-0.4,0.2)
    motor.stop(0.1)
    distance=calcDistance()
    return 'true'


@app.route('/right_side')

def right_side():
    print ("RIGHT")
    
    motor.move(0.6,0.4,0.2)
    motor.stop(0.1)
    distance=calcDistance()
    return 'true'



@app.route('/up_side')

def up_side():
    print ("FORWARD")
    motor.move(0.6,0,0.2)
    motor.stop(0.1)
    distance=calcDistance()
    return 'true'


@app.route('/down_side')

def down_side():
    print ("BACK")
    motor.move(-0.6,0,0.2)
    motor.stop(0.1)
    distance=calcDistance()
    return 'true'

 



if __name__ == '__main__':
    app.run()

camera.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
