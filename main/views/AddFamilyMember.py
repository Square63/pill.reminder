from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.MemberSerializer import MemberSerializer

class AddFamilyMember(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    def post(self, request, *args, **kwargs):
        form_data = self.request.data
        form_data['family'] = request.user.userprofile.family
        member_serializer = self.serializer_class(data=form_data, context=request.user)
        print(form_data)
        if member_serializer.is_valid():
            member_serializer.save()
            return Response({'message': 'Member has been added.'}, status=status.HTTP_200_OK)
        else:
            return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

add_family_member = AddFamilyMember.as_view()
