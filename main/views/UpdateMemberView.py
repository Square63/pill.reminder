from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.MemberSerializer import MemberSerializer

class UpdateMemberView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    def put(self, request, pk=None):
        form_data = request.data
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            user = None
        if user is not None:
            member_serializer = self.serializer_class(user, data=form_data, partial=True, context={'request': request})
            if not member_serializer.is_valid():
                return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            member_serializer.save()
            return Response({'message': 'Member updated.'}, status=status.HTTP_200_OK)

member_edit = UpdateMemberView.as_view()
