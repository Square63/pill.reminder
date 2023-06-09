from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, UserUpdateForm, AddReminderForm, EditReminderForm, EditMedicineForm, MedicineFormSet, EditMedicineFormSet
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reminder, DAYS_CHOICES, Medicine

# Create your views here.
def home(request):
    base_template = 'pillreminder/base.html'
    if request.user.is_authenticated:
        base_template = 'pillreminder/dashboard.html'
    else:
        return redirect(reverse_lazy('login'))
    return render(request, 'pillreminder/home.html', {'base_template': base_template})

class SignUp(CreateView):
    model = User
    template_name = 'pillreminder/signup.html'
    success_url = reverse_lazy("login")
    form_class = SignUpForm

@login_required
def profile(request):
    base_template = 'pillreminder/base.html'
    if request.user.is_authenticated:
        base_template = 'pillreminder/dashboard.html'
    return render(request, 'pillreminder/profile.html', {'base_template': base_template})

class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'pillreminder/profile-edit.html'
    success_url = reverse_lazy("profile")
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user

class AddReminder(LoginRequiredMixin, CreateView):
    model = Reminder
    template_name = 'pillreminder/add-reminder.html'
    success_url = reverse_lazy("home")
    form_class = AddReminderForm

    def get(self, *args, **kwargs):
        formset = MedicineFormSet()
        form = AddReminderForm()
        form.formset = formset
        return self.render_to_response({'form': form})

    def post(self, *args, **kwargs):
        form = AddReminderForm(self.request.POST)
        form.formset = MedicineFormSet(self.request.POST)
        if form.is_valid() and form.formset.is_valid():
            reminder = Reminder()
            reminder.is_active = form.cleaned_data['is_active']
            reminder.days = form.cleaned_data['days']
            reminder.time = form.clean_time()
            reminder.user = self.request.user
            reminder.save()
            for med_sub in form.formset.cleaned_data:
                medicine = Medicine()
                medicine.name = med_sub['name']
                medicine.dosage = med_sub['dosage']
                medicine.reminder = reminder
                medicine.save()
            messages.success(self.request, 'The reminder has been created.')
            return redirect(reverse_lazy('home'))
        else:
            return self.render_to_response({'form': form})

@login_required
def reminder_details(request, pk):
    reminder = Reminder.objects.get(id=pk)
    return render(request, 'pillreminder/reminder-details.html', {'reminder': reminder})

class EditReminder(LoginRequiredMixin, UpdateView):
    model = Reminder
    template_name = 'pillreminder/edit-reminder.html'
    success_url = reverse_lazy("home")
    form_class = EditReminderForm
    def get(self, *args, **kwargs):
        reminder = Reminder.objects.get(id=kwargs.pop('pk'))
        medicines = []
        for medicine in reminder.medicine_set.all():
            medicines.append({ "id": medicine.id, "name": medicine.name, "dosage": medicine.dosage })
        medicineFormset = formset_factory(EditMedicineForm, extra=0)
        formset = medicineFormset(initial=medicines)
        form = EditReminderForm(instance=reminder)
        form.formset = formset
        return self.render_to_response({'form': form})

    def post(self, *args, **kwargs):
        reminder = Reminder.objects.get(id=kwargs.pop('pk'))
        form = EditReminderForm(self.request.POST)
        form.formset = EditMedicineFormSet(self.request.POST)
        if form.is_valid() and form.formset.is_valid():
            reminder.is_active = form.cleaned_data['is_active']
            reminder.days = form.cleaned_data['days']
            reminder.time = form.clean_time()
            reminder.user = self.request.user
            reminder.save()
            for med_sub in form.formset.cleaned_data:
                medicine = Medicine.objects.get(id=med_sub['id'])
                medicine.name = med_sub['name']
                medicine.dosage = med_sub['dosage']
                medicine.reminder = reminder
                medicine.save()
            messages.success(self.request, 'The reminder has been updated.')
            return redirect(reverse_lazy('home'))
        else:
            return self.render_to_response({'form': form})
