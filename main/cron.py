from .models import UserMethods as User
from .mail import send_reminder_email
from .phone import make_phone_call
from datetime import datetime, timedelta

def send_reminder():
    users = User.objects.all()
    for user in users:
        reminders = user.next_reminders()
        if reminders:
            for reminder in reminders:
                hour = datetime.now().strftime('%H:%M:%S')
                one_hour_later = datetime.now() + timedelta(hours=1)
                one_hour_later = one_hour_later.strftime('%H:%M:%S')
                remindertypes = reminder.remindertype_set.filter(time__range=(hour, one_hour_later))
                for remindertype in remindertypes:
                    if remindertype.type == 'email':
                        send_reminder_email(user, reminder, remindertype)
                    if remindertype.type == 'phone_call':
                        make_phone_call(user.userprofile.phone.number, remindertype.id)
