from django.contrib import admin
from .models import Reminder, Medicine

# Register your models here.
admin.site.register(Reminder)
admin.site.register(Medicine)
