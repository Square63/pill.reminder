from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class LoginSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField('_get_access_token')
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'tokens')
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.pop('password')
        try:
            name = email.split('@')[0]
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            user = None
        if user is None:
            raise serializers.ValidationError("Account with given credentials does not exist.")
        if user:
            authenticate_user = authenticate(username=user.username, password=password)
            if authenticate_user is None:
                raise serializers.ValidationError("Email or Password is wrong.")
        return attrs
    def create(self, validated_data):
        name = validated_data['email'].split('@')[0]
        user = User.objects.get(username=name)
        user.last_login = timezone.now()
        user.save()
        return user
    def _get_access_token(self, user_object):
        refresh = RefreshToken.for_user(user_object)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
