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
