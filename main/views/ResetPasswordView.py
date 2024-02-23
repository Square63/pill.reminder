from rest_framework import generics, status, response
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ..serializers.EmailSerializer import EmailSerializer
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from ..models import PasswordToken

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    def post(self, request):
        serialzer = self.serializer_class(data=request.data)
        serialzer.is_valid(raise_exception=True)
        user_email = serialzer.data['email']
        user = User.objects.get(email=user_email)
        token = PasswordResetTokenGenerator().make_token(user=user)
        mail_subject = 'RxTick - Password Reset'
        message = render_to_string('main/emails/reset_password_email.html', {
                'user': user,
                'domain': settings.FRONTEND_BASE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
        to_email = user_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        user_token = PasswordToken.objects.create(
            token=token,
            user=user
        )
        user_token.save()
        return response.Response({'message': 'An email has been send with password reset instructions.'}, status=status.HTTP_200_OK)

reset_password_view = ResetPasswordView.as_view()
