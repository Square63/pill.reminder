from rest_framework import serializers
from datetime import datetime
from ..models import ReminderType, REMINDER_CHOICES

class ReminderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderType
        fields = '__all__'
    def to_representation(self, instance):
        data = super(ReminderTypeSerializer, self).to_representation(instance)
        data['object'] = datetime.strptime(instance.time, '%H:%M')
        reminder_choices  = {key: value for key, value in REMINDER_CHOICES}
        data['type_normal'] = reminder_choices.get(instance.type)
        return data
