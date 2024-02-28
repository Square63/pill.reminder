from ..models import Family, UserProfile
from rest_framework import serializers

class FamilySerializer(serializers.Serializer):
  class Meta:
    model = UserProfile
    fields = '__all__'
  def to_representation(self, instance):
    data =  super(FamilySerializer, self).to_representation(instance)
    return data
