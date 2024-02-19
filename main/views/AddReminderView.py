from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.ReminderSerializer import ReminderSerializer
from ..serializers.MedicineSerializer import MedicineSerializer
from ..serializers.ReminderTypeSerializer import ReminderTypeSerializer
from datetime import datetime
import json

class AddReminderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReminderSerializer
    def get_time(self):
        hours = self.request.data.get('hours')
        minutes = self.request.data.get('minutes')
        if int(hours) < 10 and len(hours) == 1:
            hours = '0'+str(hours)
        if int(minutes) < 10 and len(minutes) == 1:
            minutes = '0'+str(minutes)
        time_12_format = hours+':'+minutes+self.request.data.get('ampm')
        return datetime.strptime(time_12_format, '%I:%M%p').time()

    def post(self, request, *arg, **kwargs):
        form_data = self.request.data
        medicines = form_data.get('medicines')
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
        form_data['time'] = str(self.get_time())
        form_data['days'] = ', '.join(form_data['days'])
        reminder_serializer = self.serializer_class(data=form_data)
        if reminder_serializer.is_valid():
            instance = reminder_serializer.save()
        else:
            return Response(reminder_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        form_data['reminder'] = instance.id
        reminder_type_serializer = ReminderTypeSerializer(data=form_data)
        if reminder_type_serializer.is_valid():
            reminder_type_serializer.save()
        else:
            return Response(reminder_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        medicines = form_data.get('medicines')
        medicines = json.loads(medicines)
        for medicine in medicines:
            medicine['reminder'] = instance.id
            medicine['dosage'] = int(medicine['dosage'])
        medicines_serializer = MedicineSerializer(data=medicines, many=True)
        medicines_serializer.is_valid(raise_exception=True)
        medicines_serializer.save()
        return Response({'message': 'Reminder has been added!'})

add_reminder_view = AddReminderView.as_view()
