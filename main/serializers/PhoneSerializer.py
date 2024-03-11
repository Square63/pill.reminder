from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Phone
from datetime import datetime

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'
    def to_representation(self, instance):
        data = super(PhoneSerializer, self).to_representation(instance)
        data['resend_in'] = round(instance.sent_on.timestamp()) - round(datetime.now().timestamp())
        return data
