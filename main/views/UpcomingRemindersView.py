from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.ReminderSerializer import ReminderSerializer
from ..models import Reminder
from ..models import UserMethods as User

class UpcomingRemindersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReminderSerializer
    def get(self, request, *arg, **kwargs):
        user = User.objects.get(id=request.user.id)
        reminders = user.upcoming_reminders()
        serializer = self.serializer_class(reminders, many=True)
        return Response(serializer.data)

upcoming_reminders_view = UpcomingRemindersView.as_view()
