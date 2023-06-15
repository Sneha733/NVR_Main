from flask import Flask, render_template, request, redirect, url_for, make_response,Response
import cv2


app=Flask(__name__)
camera=cv2.VideoCapture(0)


def generate_frames():
    while True:
        success,frame=camera.read()  ##sucess boolean fn read or not read
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
