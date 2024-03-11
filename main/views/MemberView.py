from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.UserSerializer import UserSerializer

class MemberView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            user = None
        if user is not None:
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return Response({'message': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

member_view = MemberView.as_view()
