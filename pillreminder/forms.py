from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import formset_factory
from .models import Reminder, DAYS_CHOICES, Medicine, ProfilePicture
from .validators import validate_dosage

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
    ampm = forms.ChoiceField(label=' ', choices=(('AM', 'AM'), ('PM', 'PM')), required=False)
    class Meta:
        model = Reminder
        exclude = ("user", "time", "reminded")
    def clean_days(self):
        return ', '.join(self.cleaned_data['days'])
    def clean_time(self):
        hours = self.cleaned_data['hours']
        minutes = self.cleaned_data['minutes']
        if int(hours) < 10 and len(hours) == 1:
            hours = '0'+str(hours)

        if int(minutes) < 10 and len(minutes) == 1:
            minutes = '0'+str(minutes)
        return hours + ':' + minutes + self.cleaned_data['ampm']

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
    ampm = forms.ChoiceField(label=' ', choices=(('AM', 'AM'), ('PM', 'PM')), required=False)
    class Meta:
        model = Reminder
        exclude = ("user", "time", "reminded")
    def clean_days(self):
        return ', '.join(self.cleaned_data['days'])
    def clean_time(self):
        hours = self.cleaned_data['hours']
        minutes = self.cleaned_data['minutes']
        if int(hours) < 10 and len(hours) == 1:
            hours = '0'+str(hours)

        if int(minutes) < 10 and len(minutes) == 1:
            minutes = '0'+str(minutes)
        return hours + ':' + minutes + self.cleaned_data['ampm']

class DeleteReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('id',)

class MedicineAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['required'] = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    dosage = forms.IntegerField(label='Dosage (in mg)', widget=forms.NumberInput(), validators=[validate_dosage])
    class Meta:
        model = Medicine
        fields = ("name", "dosage")

class EditMedicineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dosage'].widget.attrs['min'] = 1
        self.fields['dosage'].widget.attrs['max'] = 1000
        self.fields['dosage'].label = 'Dosage (in mg)'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    id = forms.IntegerField(widget=forms.HiddenInput())
    delete = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':0}))
    class Meta:
        model = Medicine
        fields = ("name", "dosage")

MedicineFormSet = formset_factory(
    MedicineAddForm, extra=1
)

EditMedicineFormSet = formset_factory(
    EditMedicineForm, extra=1
)

class ProfilePictureForm(forms.ModelForm):
    image = forms.ImageField(label='Profile Picture', required=False)
    class Meta:
        model = ProfilePicture
        fields = ('image', )

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    message = forms.CharField(widget=forms.Textarea())
