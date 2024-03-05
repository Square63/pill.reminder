from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.ReminderSerializer import ReminderSerializer

class RemindersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReminderSerializer
    def get(self, request, *arg, **kwargs):
        serializer = self.serializer_class(request.user.userprofile.family.reminders.all(), many=True)
        return Response(serializer.data)

reminders_view = RemindersView.as_view()
