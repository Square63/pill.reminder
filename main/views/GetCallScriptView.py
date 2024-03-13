from django.http import HttpResponse
from ..models import ReminderType

def get_call_script_view(request, pk):
    reminder_type = ReminderType.objects.get(pk=pk)
    reminder = reminder_type.reminder
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<Response>\n'
    xml_content += '    <Say voice="woman" wiid="N2">Hi there!</Say>\n'
    xml_content += '    <Pause length="1" wiid="N4"/>\n'
    xml_content += f'    <Say voice="woman" wiid="N5">Let {reminder.user.username} know that you have received this call.</Say>\n'
    xml_content += '</Response>\n'
    return HttpResponse(xml_content, content_type='application/xml')

call_script_view = get_call_script_view
