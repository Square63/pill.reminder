from rest_framework import serializers
from ..models import Reminder

class ReminderSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField('days_info')
    class Meta:
        model = Reminder
        fields = '__all__'
    def to_representation(self, instance):
        data =  super(ReminderSerializer, self).to_representation(instance)
        # data.pop('time')
        return data
    def days_info(self, obj):
        return obj.get_selected_days()
