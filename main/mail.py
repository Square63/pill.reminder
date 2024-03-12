from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def send_reminder_email(user, reminder, remindertype):
    subject = 'Pills Reminder'
    message = '<p>This is a reminder.</p>'
    htmly = get_template('main/emails/reminder.html')
    d = { 'user': user, 'reminder': reminder, 'remindertype': remindertype }
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, message, "Pills Reminder <main@square63.com>", [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print(f"Reminder was sent to {user.email}.")
