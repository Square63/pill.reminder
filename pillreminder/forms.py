from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import formset_factory
from .models import Reminder, DAYS_CHOICES, Medicine

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class AddReminderForm(forms.ModelForm):
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAYS_CHOICES)
    hours = forms.CharField(label='Hour', widget=forms.NumberInput(attrs={'min':1, 'max':12}))
    minutes = forms.CharField(label='Minutes', widget=forms.NumberInput(attrs={'min':1, 'max':59}))
    ampm = forms.ChoiceField(label=' ', choices=(('am', 'AM'), ('pm', 'PM')), required=False)
    class Meta:
        model = Reminder
        exclude = ("user", "time")
    def clean_days(self):
        return ', '.join(self.cleaned_data['days'])
    def clean_time(self):
        return self.cleaned_data['hours'] + ':' + self.cleaned_data['minutes'] + self.cleaned_data['ampm']

class EditReminderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditReminderForm, self).__init__(*args, **kwargs)
        reminder = kwargs.get('instance')
        if reminder is None:
            return
        days = []
        for day in reminder.get_days():
            days.append(day.strip())
        self.initial['days'] = days
        self.initial['hours'] = reminder.get_hours
        self.initial['minutes'] = reminder.get_minutes
        self.initial['ampm'] = reminder.get_ampm

    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAYS_CHOICES)
    hours = forms.CharField(label='Hour', widget=forms.NumberInput(attrs={'min':1, 'max':12}))
    minutes = forms.CharField(label='Minutes', widget=forms.NumberInput(attrs={'min':1, 'max':59}))
    ampm = forms.ChoiceField(label=' ', choices=(('am', 'AM'), ('pm', 'PM')), required=False)
    class Meta:
        model = Reminder
        exclude = ("user", "time")
    def clean_days(self):
        return ', '.join(self.cleaned_data['days'])
    def clean_time(self):
        return self.cleaned_data['hours'] + ':' + self.cleaned_data['minutes'] + self.cleaned_data['ampm']

class MedicineAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dosage'].widget.attrs['min'] = 1
        self.fields['dosage'].widget.attrs['max'] = 1000
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Medicine
        fields = ("name", "dosage")

class EditMedicineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dosage'].widget.attrs['min'] = 1
        self.fields['dosage'].widget.attrs['max'] = 1000
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Medicine
        fields = ("name", "dosage")

MedicineFormSet = formset_factory(
    MedicineAddForm, extra=1
)

EditMedicineFormSet = formset_factory(
    EditMedicineForm, extra=1
)
