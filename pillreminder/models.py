from django.contrib.auth.models import User
from django.db import models

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

class Reminder(models.Model):
    is_active = models.BooleanField(default=True)
    days = models.CharField(max_length=255, default="Monday")
    time = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_days(self):
        return self.days.split(',')
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
    def has_medicines(self):
        return self.medicine_set.count() > 0

class Medicine(models.Model):
    medicine = models.CharField(max_length=255)
    dosage = models.BigIntegerField()
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    def get_dosage(self):
        return str(self.dosage) + 'mg'
