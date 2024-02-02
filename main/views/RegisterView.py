from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import generics
from ..serializers.RegisterSerializer import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

register_view = RegisterView.as_view()
