from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Phone

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'
