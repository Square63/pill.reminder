from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'password2')
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
        data['family'] = instance.userprofile.family.id
        data['full_name'] = instance.get_full_name()
        data['last_login'] = instance.last_login.strftime('%Y-%m-%d %H:%M:%S') if instance.last_login is not None else None
        data['date_joined'] = instance.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        return data
    def update(self, instance, validated_data):
        for name, value in validated_data.items():
            if name == 'password':
                instance.set_password(value)
            else:
                setattr(instance, name, value)
        instance.save()
        return instance
