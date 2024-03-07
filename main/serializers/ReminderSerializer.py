from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Reminder, ReminderType
from .MedicineSerializer import MedicineSerializer
from .ReminderTypeSerializer import ReminderTypeSerializer
from .UserSerializer import UserSerializer
import json

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
    def to_representation(self, instance):
        data =  super(ReminderSerializer, self).to_representation(instance)
        medicines = instance.medicine_set.all()
        medicines = MedicineSerializer(medicines, many=True)
        times = ReminderTypeSerializer(instance.remindertype_set.all(), many=True)
        data['medicines'] = medicines.data
        data['days'] = instance.get_selected_days()
        data['days_arr'] = instance.get_stripped_days()
        data['times'] = times.data
        data['user'] = UserSerializer(instance.user).data
        data['created_at'] = instance.created_at.strftime('%a, %d %b %Y %H:%M:%S')
        data['updated_at'] = instance.updated_at.strftime('%a, %d %b %Y %H:%M:%S')
        return data
