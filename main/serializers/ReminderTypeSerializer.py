from rest_framework import serializers
from ..models import ReminderType

class ReminderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderType
        fields = '__all__'
