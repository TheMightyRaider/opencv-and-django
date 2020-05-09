from django.urls import path

from . import views, encodingview

urlpatterns=[
    path('postframes',views.videostream,name='postframes'),
    path('encoding',encodingview.generateImageEncoding.as_view(),name='encodings')
]


