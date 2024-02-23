from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is None:
            raise serializers.ValidationError('User not found.')
        return attrs
