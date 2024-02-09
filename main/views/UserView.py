from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.UserSerializer import UserSerializer
from ..models import Reminder

class UserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            user = None

        if user is not None:
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

user_view = UserView.as_view()
