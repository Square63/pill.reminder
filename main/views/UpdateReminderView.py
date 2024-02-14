from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.MedicineSerializer import MedicineSerializer
from ..serializers.ReminderSerializer import ReminderSerializer
from ..models import Reminder, Medicine
import json

class UpdateReminderView(generics.UpdateAPIView):
    queryset = Reminder.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReminderSerializer

    def get_time(self):
        hours = self.request.data.get('hours')
        minutes = self.request.data.get('minutes')
        if int(hours) < 10 and len(hours) == 1:
            hours = '0'+str(hours)
        if int(minutes) < 10 and len(minutes) == 1:
            minutes = '0'+str(minutes)
        return hours+':'+minutes+self.request.data.get('ampm')

    def put(self, request, pk=None):
        try:
            reminder = Reminder.objects.get(id=pk)
        except Reminder.DoesNotExist:
            reminder = None
        if reminder is not None:
            form_data = self.request.data
            medicines = json.loads(form_data.get('medicines'))
            if self.request.user.id:
                form_data['user'] = self.request.user.id
            errors = {}
            if form_data.get('hours') == '' or form_data.get('hours') is None:
                errors['hours'] = ['This field is required.']
            if form_data.get('minutes') == '' or form_data.get('minutes') is None:
                errors['minutes'] = ['This field is required.']
            if form_data.get('ampm') == '' or form_data.get('ampm') is None:
                errors['ampm'] = ['This field is required.']
            if form_data.get('days') == '' or form_data.get('days') is None:
                errors['days'] = ['This field is required.']
            if medicines is None:
                errors['non_field_errors'] = ['Atleast add one medicine.']
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            form_data['user'] = self.request.user.id
            form_data['time'] = self.get_time()
            form_data['days'] = ', '.join(form_data['days'])
            reminder_serializer = self.serializer_class(reminder, self.request.data)
            if reminder_serializer.is_valid():
                reminder_serializer.save()
            else:
                return Response(reminder_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            for medicine in medicines:
                if medicine['id'] == '0':
                    medicine_instance = Medicine()
                else:
                    medicine_instance = Medicine.objects.get(id=medicine['id'])
                medicine_instance.reminder = reminder
                medicine_instance.name = medicine['name']
                medicine_instance.dosage = medicine['dosage']
                medicine_instance.save()
        else:
            return Response({'error': 'Resume not found!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Reminder has been updated.'}, status=status.HTTP_200_OK)

update_reminder_view = UpdateReminderView.as_view()
