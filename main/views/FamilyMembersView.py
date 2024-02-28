from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.UserSerializer import UserSerializer
from ..models import Family, UserProfile

class FamilyMembersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request, *arg, **kwargs):
        family_users = UserProfile.objects.filter(family_id=request.user.userprofile.family.id).select_related('user').all()
        data = []
        for user in family_users:
            user_serializer = self.serializer_class(user.user)
            data.append(user_serializer.data)
        return Response(data, status=status.HTTP_200_OK)

family_members_view = FamilyMembersView.as_view()
