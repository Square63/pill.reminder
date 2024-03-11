from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from twilio.rest import Client
from ..models import Phone
import random

class VerificationSMSView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk=None):
        phone = request.data['phone']
        if phone == '' or phone is None:
            return Response({'phone_number': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=pk)

        code = random.randint(100000, 999999)

        profile = user.userprofile
        user_phone = profile.phone
        if user_phone is None:
            user_phone = Phone()
        user_phone.number = phone
        user_phone.code = code
        user_phone.save()

        profile.phone = user_phone
        profile.save()

        tw_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = '''This is your phone number activation code: {}'''.format(code)

        sms = tw_client.messages.create(
                from_='+15102395727',
                to=phone,
                body=message
            )

        print(sms.sid)

        return Response({'message': 'A verification code has been sent to your phone number.'}, status=status.HTTP_200_OK)

verification_sms_view = VerificationSMSView.as_view()
