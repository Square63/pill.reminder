from rest_framework import generics, response, status
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from ..serializers.PasswordSerializer import PasswordSerializer
from ..models import PasswordToken

class ResetPassword(generics.GenericAPIView):
    serializer_class = PasswordSerializer
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)

        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        password = request.data.get('password')

        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        user.set_password(password)
        user.save()
        user_token = PasswordToken.objects.get(token=token)
        user_token.delete()
        return response.Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)

reset_password = ResetPassword.as_view()
