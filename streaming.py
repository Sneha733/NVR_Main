from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from time import sleep
#import motor_driver
#object2 =motor_driver.Motor()
from time import sleep

#import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
print ("DOne")
import time

#motor = Motor(17,22,27,2,3,4)

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
              
            if capture:
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)

            if rec:
                rec_frame = frame
                frame = cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame = cv2.flip(frame,1)
                
                if out is not None:
                    out.write(frame)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
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
'''@app.route('/left_side')

def left_side():

    data1="LEFT"
    print ("LEFT")
    object2.move(0.6,-0.4,0.2)
    #sleep(0.5)
    #motor.stop(0.1)

    return 'true'
    


@app.route('/right_side')

def right_side():

    
    #data1="RIGHT"
    print ("RIGHT")
    object2.move(0.6,0.4,0.2)
    #sleep(0.5)
    #motor.stop(0.1)

    return 'true'



@app.route('/up_side')

def up_side():

    
    #data1="FORWARD"
    print ("FORWARD")
    object2.move(0.6,0,0.2)
    #sleep(0.5)
    #motor.stop(0.1)

    return 'true'


@app.route('/down_side')

def down_side():

   
    data1="BACK"
    print ("BACK")
    object2.move(192.0,0,0.2)
    #sleep(0.5)
    #motor.stop(0.1)

    return 'true'''

 



if __name__ == '__main__':
    app.run()
    app.run(host='192.0.0.0',port=5010)

camera.release()
cv2.destroyAllWindows()

    
