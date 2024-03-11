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

    def post(self, request, *arg, **kwargs):
        form_data = self.request.data
        medicines = form_data.get('medicines')
        form_data['family'] = request.user.userprofile.family.id
        errors = {}
        reminder_serializer = self.serializer_class(data=form_data)
        if not reminder_serializer.is_valid():
            errors.update(reminder_serializer.errors)
        if form_data.get('days') == '' or form_data.get('days') is None:
            errors['days'] = ['This field is required.']
        if medicines is None:
            errors['name0'] = ['This field is required.']
            errors['dosage0'] = ['This field is required.']
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        form_data['days'] = ', '.join(form_data['days'])
        reminder_serializer = self.serializer_class(data=form_data)
        if reminder_serializer.is_valid():
            instance = reminder_serializer.save()
        else:
            return Response(reminder_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        form_data['reminder'] = instance.id
        times = form_data.get('times')
        times = json.loads(times)
        for time in times:
            time.pop('id')
            time.pop('object')
            time['reminder'] = instance.id
        for index, time in enumerate(times):
            reminder_type_serializer = ReminderTypeSerializer(data=time)
            if reminder_type_serializer.is_valid():
                reminder_type_serializer.save()
            else:
                instance.delete()
                errors = {}
                for error in reminder_type_serializer.errors:
                    errors[error+str(index)] = reminder_type_serializer.errors[error]
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        medicines = form_data.get('medicines')
        medicines = json.loads(medicines)
        for index, medicine in enumerate(medicines):
            medicine['reminder'] = instance.id
            medicines_serializer = MedicineSerializer(data=medicine)
            if medicines_serializer.is_valid():
                medicines_serializer.save()
            else:
                errors = {}
                instance.delete()
                for error in medicines_serializer.errors:
                    errors[error+str(index)] = medicines_serializer.errors[error]
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Reminder has been added!'})

add_reminder_view = AddReminderView.as_view()
