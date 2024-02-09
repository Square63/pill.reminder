from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('_get_full_name')
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'password', 'password2', 'last_login')
    def validate(self, attrs):
        password = attrs.get('password', None)
        password2 = attrs.pop('password2', None)
        if (password is not None or password2 is not None) and (password != password2):
            raise serializers.ValidationError("Password and Confirm Password does not match.")

        return attrs
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            user = None
        if user is not None and user.id != self.context.id:
            raise serializers.ValidationError("Email already exists.")
        else:
            return value
    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        return data
    def _get_full_name(self, user_object):
        return user_object.get_full_name()
    def update(self, instance, validated_data):
        for name, value in validated_data.items():
            print(name)
            if name == 'password':
                instance.set_password(value)
            else:
                setattr(instance, name, value)
        instance.save()
        return instance
