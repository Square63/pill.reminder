from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.MedicineSerializer import MedicineSerializer
from ..serializers.ReminderSerializer import ReminderSerializer
from ..serializers.ReminderTypeSerializer import ReminderTypeSerializer
from ..models import Reminder, ReminderType, Medicine
from datetime import datetime
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
        time_12_format = hours+':'+minutes+self.request.data.get('ampm')
        return datetime.strptime(time_12_format, '%I:%M%p').time()

    def put(self, request, pk=None):
        try:
            reminder = Reminder.objects.get(id=pk)
        except Reminder.DoesNotExist:
            reminder = None
        if reminder is not None:
            form_data = self.request.data
            medicines = json.loads(form_data.get('medicines'))
            errors = {}
            if form_data.get('hours') == '' or form_data.get('hours') is None:
                errors['hours'] = ['This field is required.']
            if form_data.get('minutes') == '' or form_data.get('minutes') is None:
                errors['minutes'] = ['This field is required.']
            if form_data.get('ampm') == '' or form_data.get('ampm') is None:
                errors['ampm'] = ['This field is required.']
            if form_data.get('days') == '' or form_data.get('days') is None or not form_data.get('days'):
                errors['days'] = ['This field is required.']
            if medicines is None:
                errors['non_field_errors'] = ['Atleast add one medicine.']
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            form_data['family'] = self.request.user.userprofile.family.id
            form_data['time'] = str(self.get_time())
            form_data['days'] = ', '.join(form_data['days'])
            reminder_serializer = self.serializer_class(reminder, self.request.data)
            reminder_validated = False
            if reminder_serializer.is_valid():
                reminder_validated = True
            else:
                return Response(reminder_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            form_data['reminder'] = reminder.id
            reminder_type = reminder.get_reminder_type()
            if reminder_type is None:
                form_data['reminder'] = reminder.id
                reminder_type_serializer = ReminderTypeSerializer(data=form_data)
                reminder_type_serializer.is_valid(raise_exception=True)
                reminder_type_serializer.save()

            for index, medicine in enumerate(medicines):
                if medicine['id'] == '0':
                    medicine_instance = Medicine()
                else:
                    medicine_instance = Medicine.objects.get(id=medicine['id'])
                medicine_instance.reminder = reminder
                medicine_instance.name = medicine['name']
                medicine_instance.dosage = medicine['dosage']
                medicine_serializer = MedicineSerializer(medicine_instance, data=medicine)
                if medicine_serializer.is_valid() and reminder_validated:
                    reminder_serializer.save()
                    medicine_instance.save()
                else:
                    errors = {}
                    for error in medicine_serializer.errors:
                        errors[error+str(index)] = medicine_serializer.errors[error]
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            current_medicine_ids = list(reminder.medicine_set.values_list('id', flat=True))
            incoming_medicine_ids = [medicine['id'] for medicine in medicines]
            medicines_to_remove_ids = [medicine_id for medicine_id in current_medicine_ids if medicine_id not in incoming_medicine_ids]
            for medicine_id in medicines_to_remove_ids:
                medicine = Medicine.objects.get(id=medicine_id)
                medicine.delete()

        else:
            return Response({'error': 'Resume not found!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Reminder has been updated.'}, status=status.HTTP_200_OK)

update_reminder_view = UpdateReminderView.as_view()
