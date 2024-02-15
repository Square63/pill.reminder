from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def send_reminder_email(user, reminders):
    subject = 'Pill Reminder'
    message = '<p>This is a reminder.</p>'
    htmly = get_template('main/emails/reminder.html')
    d = { 'reminders': reminders }
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, message, "main@square63.com", [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('Reminder was sent.')