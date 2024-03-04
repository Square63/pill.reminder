from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.AccountSerializer import AccountSerializer

class UpdateAccountView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    def patch(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            user = None
        if user is not None:
            user_serializer = self.serializer_class(user, data=self.request.data, partial=True, context=request.user)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({ 'message': 'Account updated.' })
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

update_account_view = UpdateAccountView.as_view()
