from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta

# Create your models here.
DAYS_CHOICES = [
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
]

class UserMethods(User):
    def upcoming_reminders(self):
        day = datetime.now().strftime('%A')
        reminders = self.reminder_set.filter(is_active=1, days__contains=day, time__range=('00:00am', '23:59pm'), reminded=False)
        return reminders
    def next_reminders(self):
        day = datetime.now().strftime('%A')
        hours = datetime.now().strftime('%I:%M%p')
        one_hour_later = datetime.now() + timedelta(hours=1)
        one_hour_later = one_hour_later.strftime('%I:%M%p')
        reminders = self.reminder_set.filter(is_active=1, days__contains=day, time__range=(hours, one_hour_later), reminded=False)
        return reminders
    class Meta:
        proxy=True

class ProfilePicture(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Reminder(models.Model):
    is_active = models.BooleanField(default=True)
    days = models.CharField(max_length=255, default="Monday")
    time = models.CharField(max_length=20)
    reminded = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ('-id',)
    def get_days(self):
        return self.days.split(',')
    def get_stripped_days(self):
        days = []
        for day in self.get_days():
            days.append(day.strip())
        return days
    def get_hours(self):
        return self.time.split(':')[0]
    def get_minutes(self):
        minutes = self.time.split(':')[1]
        size = len(minutes)
        return minutes[:size - 2]
    def get_ampm(self):
        minutes = self.time.split(':')[1]
        size = len(minutes)
        return minutes[size - 2:]
    def get_selected_days(self):
        days = []
        for day, i in DAYS_CHOICES:
            days.append(i)
        string = self.days
        if days == self.get_stripped_days():
            string = 'Every Day'
        return string
    def has_medicines(self):
        return self.medicine_set.count() > 0
    def get_user_email(self):
        return self.user.email
    get_user_email.short_description = 'Email'
    def __str__(self):
        return self.get_selected_days() + ' @ ' + self.time

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.BigIntegerField()
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    def get_dosage(self):
        return str(self.dosage) + 'mg'
    def get_user(self):
        return self.reminder.user.username
    get_user.short_description = 'User'
    def __str__(self):
        return self.name + " " + self.get_dosage()
