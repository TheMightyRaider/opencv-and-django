from django.shortcuts import render
from django.http import StreamingHttpResponse
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2

# Create your views here.

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
print(detector)

def postframes():
    
    camera=VideoStream(src=-1).start()
    time.sleep(2)

    fps=FPS().start()

    while True:
        frame = camera.read()
        frame = imutils.resize(frame, width=500)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        print(boxes)

        if boxes is not None:
            yield '{"success":True}'
        else:
            yield "{'success':False}"


def videostream(request):
    return StreamingHttpResponse(postframes())
        



