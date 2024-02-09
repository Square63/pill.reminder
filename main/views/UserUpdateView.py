from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.UserSerializer import UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            user = None
        if user is not None:
            user_serializer = self.serializer_class(user, data=self.request.data, context=request.user)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({ 'message': 'Profile has been updated.' })
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

user_update_view = UserUpdateView.as_view()
