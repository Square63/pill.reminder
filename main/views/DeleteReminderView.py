from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Reminder

class DeleteReminderView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk=None):
        try:
            reminder = Reminder.objects.get(id=pk)
        except Reminder.DoesNotExist:
            reminder = None
        if reminder is not None:
            reminder.delete()
            return Response({'message': 'Reminder has been deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response('Reminder not found', status=status.HTTP_404_NOT_FOUND)

delete_reminder_view = DeleteReminderView.as_view()
