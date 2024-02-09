from rest_framework import serializers
from ..models import Reminder
from .MedicineSerializer import MedicineSerializer

class ReminderSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField('_days_info')
    medicines = serializers.SerializerMethodField('_get_medicines')
    class Meta:
        model = Reminder
        fields = '__all__'
    def to_representation(self, instance):
        data =  super(ReminderSerializer, self).to_representation(instance)
        return data
    def _days_info(self, resume_object):
        return resume_object.get_selected_days()
    def _get_medicines(self, resume_object):
        medicines = resume_object.medicine_set.all()
        medicines_serializer = MedicineSerializer(medicines, many=True)
        return medicines_serializer.data
