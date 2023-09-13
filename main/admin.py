from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Reminder, Medicine, DAYS_CHOICES

# Register your models here.
class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'
    def lookups(self, request, model_admin):
        return ((),)
    def choices(self, changelist):
        return next(super().choices(changelist))

class MedicineNameFilter(InputFilter):
    parameter_name = 'medicine-name'
    title = _('Medicine Name')
    def queryset(self, request, queryset):
        name = self.value()
        if name is not None:
            return queryset.filter(
                name__contains = name.strip()
            )

class DaysFilter(admin.SimpleListFilter):
    title = 'Filter by Day'
    parameter_name = 'days'
    def lookups(self, request, model_admin):
        return DAYS_CHOICES
    def queryset(self, request, queryset):
        if self.value() is not None:
            print(queryset)
            day = self.value()
            return queryset.filter(
                days__contains = day
            )
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'get_user_email', 'is_active')
    list_filter = ('is_active', DaysFilter)
    search_fields = ('user__username',)

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'reminder', 'get_user')
    list_filter = (MedicineNameFilter,)

admin.site.register(Reminder, ReminderAdmin)
admin.site.register(Medicine, MedicineAdmin)
