from rest_framework import serializers
from .models import UserAndEncodingDetail

class EncodingSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAndEncodingDetail
        fields='__all__'
    