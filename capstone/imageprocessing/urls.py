from django.urls import path

from .import views

urlpatterns=[
    path('postframes',views.videostream,name='postframes')
]