from django.shortcuts import render
from django.http import StreamingHttpResponse
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import time
import json
import cv2

from .models import UserAndEncodingDetail
# Create your views here.

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
db_encoding=UserAndEncodingDetail.objects.values_list('encoding',flat=True)
encoded_user_name=UserAndEncodingDetail.objects.values_list('person_name',flat=True)
encoding_array=[]
encoded_user_array=list(encoded_user_name)
for encoding in db_encoding:
    json_to_list=json.loads(encoding)
    encoding_array.append(json_to_list)

def postframes():
    
    camera=VideoStream(src=-1).start()
    time.sleep(2)

    fps=FPS().start()
    while True:
        obj={'recognised_name':'Unknown'}
        frame = camera.read()
        frame = imutils.resize(frame, width=500)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        encodings = face_recognition.face_encodings(rgb, boxes)
        names=[]

        for encoding in encodings:
            matches = face_recognition.compare_faces(encoding_array,encoding)
            name='Unknown'

            if True in matches:
                matchedIdxs=[i for (i,b) in enumerate(matches) if b ]
                counts={}

                for i in matchedIdxs:
                    name=encoded_user_name[i]
                    counts[name]=counts.get(name,0)+1

                name=max(counts,key=counts.get)
            
            names.append(name)
            obj['recognised_name']=name

        if names is not None:
            yield obj
        else:
            yield "{'success':False}"
        
    


def videostream(request):
    return StreamingHttpResponse(postframes())
        



