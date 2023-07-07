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
