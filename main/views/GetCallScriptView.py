from django.http import HttpResponse, HttpResponseNotFound
from ..models import ReminderType

def get_call_script_view(request, pk):
    try:
        reminder_type = ReminderType.objects.get(pk=pk)
    except ReminderType.DoesNotExist:
        reminder_type = None
    if reminder_type is not None:
        reminder = reminder_type.reminder
        user = reminder.user
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<Response>\n'
        xml_content += f'    <Say voice="woman" wiid="N2">Hi {user.first_name}!</Say>\n'
        xml_content += '    <Pause length="1" wiid="N4"/>\n'
        xml_content += f'    <Say voice="woman" wiid="N5">This is a reminder to take your following medicines at {reminder_type.get_time()} today.</Say>\n'
        for medicine in reminder.medicine_set.all():
            xml_content += f'<Say voice="woman">{medicine.name} x {medicine.get_dosage()}</Say>'
        xml_content += '</Response>\n'
        return HttpResponse(xml_content, content_type='application/xml')
    else:
        return HttpResponseNotFound('<h1>Page not found.</h1>')



call_script_view = get_call_script_view
