from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms.fields import Field
from .models import Reminder, DAYS_CHOICES

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
        days = []
        for day in reminder.get_days():
            days.append(day.strip())
        self.initial['days'] = days
        self.fields['hours'] = forms.CharField(label='Hour', widget=forms.NumberInput(attrs={'min':1, 'max':12}), initial=reminder.get_hours)
        self.fields['minutes'] = forms.CharField(label='Minutes', widget=forms.NumberInput(attrs={'min':1, 'max':59}), initial=reminder.get_minutes)
        self.fields['ampm'] = forms.ChoiceField(label=' ', choices=(('am', 'AM'), ('pm', 'PM')), required=False, initial=reminder.get_ampm)

    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAYS_CHOICES)
    class Meta:
        model = Reminder
        exclude = ("user", "time")
    def clean_days(self):
        return ', '.join(self.cleaned_data['days'])
    def clean_time(self):
        return self.cleaned_data['hours'] + ':' + self.cleaned_data['minutes'] + self.cleaned_data['ampm']
