from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

# Create your views here.


def postframes():
    camera=cv2.VideoCapture(0)
    while True:
        success,image=camera.read()
        ret,jpeg=cv2.imencode('.jpg',image)
        print(jpeg.tobytes())

        if jpeg is not None:
            yield '{"success":True}'
        else:
            yield "{'success':False}"


def videostream(request):
    return StreamingHttpResponse(postframes())
        