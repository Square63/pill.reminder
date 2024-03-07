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
        if form_data.get('days') == '' or form_data.get('days') is None:
            errors['days'] = ['This field is required.']
        if medicines is None:
            errors['non_field_errors'] = ['Atleast add one medicine.']
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
        reminder_type_serializer = ReminderTypeSerializer(data=times, many=True)
        reminder_type_serializer.is_valid(raise_exception=True)
        reminder_type_serializer.save()
        medicines = form_data.get('medicines')
        medicines = json.loads(medicines)
        for medicine in medicines:
            medicine['reminder'] = instance.id
        medicines_serializer = MedicineSerializer(data=medicines, many=True)
        medicines_serializer.is_valid(raise_exception=True)
        medicines_serializer.save()
        return Response({'message': 'Reminder has been added!'})

add_reminder_view = AddReminderView.as_view()
