from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.ReminderSerializer import ReminderSerializer
from ..models import Reminder

class ReminderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReminderSerializer
    def get(self, request, pk=None):
        try:
            reminder = Reminder.objects.get(pk=pk)
        except Reminder.DoesNotExist:
            reminder = None

        if reminder is not None:
            serializer = self.serializer_class(reminder)
            return Response(serializer.data)
        else:
            return Response({'message': 'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)

reminder_view = ReminderView.as_view()
