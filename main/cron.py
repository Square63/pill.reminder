from .models import UserMethods as User
from .mail import send_reminder_email

def send_reminder():
    users = User.objects.all()
    for user in users:
        reminders = user.next_reminders()
        if reminders:
            send_reminder_email(user, reminders)
