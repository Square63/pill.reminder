from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.ChangePasswordSerializer import ChangePasswordSerializer

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def patch(self, request, *args, **kwargs):
        password_serializer = self.serializer_class(data=self.request.data, context={'user': request.user})
        if password_serializer.is_valid():
            password_serializer.update(password_serializer.validated_data)
            return Response({'message': 'Password updated.'}, status=status.HTTP_200_OK)
        else:
            return Response(password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


change_password_serializer = ChangePasswordView.as_view()
