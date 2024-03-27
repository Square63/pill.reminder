from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..serializers.GoogleAuthSerializer import GoogleAuthSerializer

class GoogleSignInView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleAuthSerializer

google_signin_view = GoogleSignInView.as_view()
