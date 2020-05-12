from django.urls import path

from . import views, encodingview

urlpatterns=[
    path('postframes',views.videostream.as_view(),name='postframes'),
    path('encoding',encodingview.generateImageEncoding.as_view(),name='encodings'),
    path('',views.index.as_view(),name='index')
]


