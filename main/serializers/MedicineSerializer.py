from rest_framework import serializers
from ..models import Medicine
import json

class MedicineSerializer(serializers.ModelSerializer):
  class Meta:
    model = Medicine
    fields = '__all__'
  def to_representation(self, instance):
    data =  super(MedicineSerializer, self).to_representation(instance)
    return data
