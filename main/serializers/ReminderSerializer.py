from rest_framework import serializers
from ..models import Reminder, ReminderType
from .MedicineSerializer import MedicineSerializer
from .ReminderTypeSerializer import ReminderTypeSerializer
import json

class ReminderSerializer(serializers.ModelSerializer):
    hours = serializers.SerializerMethodField('_get_hours')
    minutes = serializers.SerializerMethodField('_get_minutes')
    class Meta:
        model = Reminder
        fields = '__all__'
    def to_representation(self, instance):
        data =  super(ReminderSerializer, self).to_representation(instance)
        medicines = instance.medicine_set.all()
        medicines = MedicineSerializer(medicines, many=True)
        data['medicines'] = medicines.data
        data['days'] = instance.get_selected_days()
        data['days_arr'] = instance.get_stripped_days()
        data['ampm'] = instance.get_ampm()
        data['time'] = instance.get_time()
        data['reminder_type'] = ReminderTypeSerializer(instance.get_reminder_type()).data['reminder_type']
        return data
    def _get_hours(self, reminder_object):
        return reminder_object.get_hours()
    def _get_minutes(self, reminder_object):
        return reminder_object.get_minutes()
