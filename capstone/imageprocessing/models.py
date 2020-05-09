from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class UserAndEncodingDetail(models.Model):
    encoding=models.TextField(models.FloatField())
    person_name=models.CharField(max_length=20,default='admin')

    def __str__(self):
        return self.person_name