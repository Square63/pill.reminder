from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
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

REMINDER_CHOICES = [
    ("email", "Email"),
    ("phone_call", "Phone Call"),
    ("whatsapp", "WhatsApp")
]

class UserMethods(User):
    def upcoming_reminders(self):
        day = datetime.now().strftime('%A')
        reminders = self.reminder_set.filter(is_active=1, days__contains=day, time__range=('00:00am', '23:59pm'), reminded=False)
        return reminders
    def next_reminders(self):
        day = datetime.now().strftime('%A')
        hour = datetime.now().strftime('%H:%M:%S')
        one_hour_later = datetime.now() + timedelta(hours=1)
        one_hour_later = one_hour_later.strftime('%H:%M:%S')
        reminders = self.reminder_set.filter(is_active=1, days__contains=day, time__range=(hour, one_hour_later), reminded=False)
        return reminders
    class Meta:
        proxy=True

class Family(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

class Phone(models.Model):
    number = models.CharField(max_length=20, null=True, blank=True)
    code = models.BigIntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.ForeignKey(Phone, on_delete=models.SET_NULL, null=True, blank=True)

class ProfilePicture(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Reminder(models.Model):
    title = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    days = models.CharField(max_length=255, default="Monday")
    reminded = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, related_name='reminders')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('-id',)
    def get_days(self):
        return self.days.split(',')
    def get_stripped_days(self):
        days = []
        for day in self.get_days():
            days.append(day.strip())
        return days
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
    def get_reminder_type(self):
        return self.remindertype if hasattr(self, 'remindertype') else None
    def __str__(self):
        return self.get_days()
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    def get_dosage(self):
        return str(self.dosage) + 'mg'
    def get_user(self):
        return self.reminder.user.username
    get_user.short_description = 'User'
    def __str__(self):
        return self.name + " " + self.get_dosage()

class ReminderType(models.Model):
    type = models.CharField(max_length=255, choices=REMINDER_CHOICES, default="email")
    time = models.CharField(max_length=20)
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.type

class PasswordToken(models.Model):
  token = models.CharField(max_length=255)
  used = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
