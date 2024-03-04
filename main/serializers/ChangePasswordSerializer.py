from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)
    def validate(self, attrs):
        current_password = attrs.pop('current_password')
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        user = User.objects.get(id=self.context['user'].id)
        if check_password(current_password, user.password) is False:
            raise serializers.ValidationError("Current password is wrong.")
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password do not match.")
        return attrs
    def update(self, validated_data):
        user = User.objects.get(id=self.context['user'].id)
        user.set_password(validated_data['password'])
        user.save()
        return self.context['user']
