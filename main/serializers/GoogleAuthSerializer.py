from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import EmailValidator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Family, UserProfile

class GoogleAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    tokens = serializers.SerializerMethodField('_get_access_token')
    def check_family(self, user):
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
        if profile is None:
            family = Family.objects.create()
            family.save()
            UserProfile.objects.create(user=user, family=family)
    def create(self, validated_data):
        request = self.context['request']
        try:
            user = User.objects.get(email=validated_data['email'])
        except User.DoesNotExist:
            user = None

        if user is None:
            name = validated_data['email'].split('@')[0]
            user = User.objects.create(
                username = name,
                email = validated_data['email']
            )
            user.first_name = request.data.get('given_name')
            user.last_name = request.data.get('family_name')

        user.last_login = timezone.now()
        user.save()
        self.check_family(user)
        return user
    def _get_access_token(self, user_object):
        refresh = RefreshToken.for_user(user_object)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
