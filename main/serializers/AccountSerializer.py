from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    email_changed = serializers.BooleanField(required=True)
    def validate(self, attrs):
        print(attrs)
        email = attrs.get('email')
        email_changed = attrs.get('email_changed')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None and email_changed is True:
            raise serializers.ValidationError("Email already exists.")
        return attrs
    def update(self, instance, validated_data):
        for name, value in validated_data.items():
            if name != 'password':
                setattr(instance, name, value)
        instance.save()
        return instance
