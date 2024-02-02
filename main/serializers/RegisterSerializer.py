from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField('_get_access_token')
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'access')
    def validate(self, attrs):
        email = attrs.get('email')
        password=attrs.get('password')
        password2=attrs.pop('password2')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            raise serializers.ValidationError("Account with this email already register.")

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does not match.")
        return attrs
    def create(self, validated_data):
        name = validated_data['email'].split('@')[0]
        user = User.objects.create(
            username = name,
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user
    def _get_access_token(self, user_object):
        refresh = RefreshToken.for_user(user_object)
        return str(refresh.access_token)
