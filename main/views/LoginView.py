from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import generics
from ..serializers.LoginSerializer import LoginSerializer

class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

login_view = LoginView.as_view()
