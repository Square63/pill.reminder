from rest_framework import serializers
from ..models import Medicine
import json

class MedicineSerializer(serializers.ModelSerializer):
  dosage = serializers.SerializerMethodField('_get_dosage')
  class Meta:
    model = Medicine
    fields = '__all__'
  def to_representation(self, instance):
    data =  super(MedicineSerializer, self).to_representation(instance)
    return data
  def _get_dosage(self, medicine_object):
    return medicine_object.get_dosage()
