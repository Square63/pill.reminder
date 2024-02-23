from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import serializers

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)
    def validate(self, attrs):
        uidb64 = self.context['kwargs'].get('uidb64')
        token = self.context['kwargs'].get('token')
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None or PasswordResetTokenGenerator().check_token(user, token) is False:
            raise serializers.ValidationError('Token has expired.')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does not match.")
        return attrs
