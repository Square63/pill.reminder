from rest_framework import serializers
from ..models import Reminder
from .MedicineSerializer import MedicineSerializer
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
        return data
    def _get_hours(self, reminder_object):
        return reminder_object.get_hours()
    def _get_minutes(self, reminder_object):
        return reminder_object.get_minutes()
