from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from twilio.rest import Client
from ..models import Phone
import random

class VerifyCodeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk=None):
        code = request.data['code']
        if code == '' or code is None:
            return Response({'code': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=pk)

        profile = user.userprofile

        if profile.phone.code != int(code):
            return Response({'code': 'The code is invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        user_phone = profile.phone
        user_phone.code = None
        user_phone.verified = True
        user_phone.save()

        profile.phone = user_phone
        profile.save()

        return Response({'message': 'Your phone number has been verified.'}, status=status.HTTP_200_OK)

verify_code_view = VerifyCodeView.as_view()
