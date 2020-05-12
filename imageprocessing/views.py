from django.shortcuts import render
from django.http import StreamingHttpResponse,JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import time
import json
import cv2
import os

from .models import UserAndEncodingDetail
# Create your views here.

class index(APIView):
    def get(self,request):
        success={
            'status':'Server is running!'
        }
        return Response(success)

def postframes():    
    db_encoding=UserAndEncodingDetail.objects.values_list('encoding',flat=True)
    encoded_user_name=UserAndEncodingDetail.objects.values_list('person_name',flat=True)
    encoding_array=[]
    encoded_user_array=list(encoded_user_name)
    for encoding in db_encoding:
        json_to_list=json.loads(encoding)
        encoding_array.append(json_to_list)

    camera=VideoStream(src=-1).start()
    time.sleep(2)
    fps=FPS().start()

    while True:
        obj={'recognised_name':'Unknown'}
        frame = camera.read()
        frame = imutils.resize(frame, width=500)
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations=face_recognition.face_locations(rgb)

        encodings = face_recognition.face_encodings(rgb, face_locations)
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
        
class videostream(APIView):
    def get(self,request):
        return StreamingHttpResponse(postframes())
        



