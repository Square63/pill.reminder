from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('_get_full_name')
    class Meta:
        model = User
        fields = '__all__'
    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.pop('is_superuser')
        data.pop('groups')
        data.pop('user_permissions')
        data.pop('password')
        data.pop('is_staff')
        return data
    def _get_full_name(self, user_object):
        return user_object.get_full_name()
