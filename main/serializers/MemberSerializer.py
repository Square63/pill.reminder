from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from rest_framework import serializers
from ..models import Phone, UserProfile
from .UserSerializer import UserSerializer

class MemberSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    phone_number = serializers.CharField(required=True)
    def validate(self, attrs):
        email = attrs.get('email')
        request = self.context['request']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if self.context and request.method == 'PUT':
            if user is not None and user != request.user:
                raise serializers.ValidationError("Email already exists.")
        elif user is not None:
            raise serializers.ValidationError("Email already exists.")
        return attrs
    def create(self, validated_data):
        name = validated_data['email'].split('@')[0]
        full_name = validated_data['full_name'].split(' ')
        user = User.objects.create(
            username = name,
            email = validated_data['email']
        )
        user.first_name = full_name[0]
        user.last_name = full_name[1]
        user.is_active = True
        user.save()
        request = self.context['request']
        phone = Phone.objects.create(number=validated_data['phone_number'], verified=False)
        userprofile = UserProfile.objects.create(user=user, family=request.user.userprofile.family, phone=phone)
        userprofile.save()
        return user
    def update(self, instance, validated_data):
        full_name = validated_data['full_name'].split(' ')
        instance.first_name = full_name[0]
        instance.last_name = full_name[1]
        instance.email = validated_data['email']
        instance.save()

        user_phone = Phone.objects.get(pk=instance.userprofile.phone.id)
        user_phone.number = validated_data['phone_number']
        user_phone.verified = not self.context['request'].data['phone_changed']
        user_phone.save()

        return instance
    def to_representation(self, instance):
        user_serializer = UserSerializer(instance)
        return user_serializer.data
