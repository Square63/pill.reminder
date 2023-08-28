from .models import UserMethods as User
from django.core.mail import send_mail

def send_reminder():
    users = User.objects.all()
    for user in users:
        if user.upcoming_reminders():
            send_mail(
                "Pills Reminder",
                "This is a reminder to take your pills.",
                "pillreminder@square63.com",
                [user.email],
                fail_silently=False,
            )
