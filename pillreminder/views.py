from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, UserUpdateForm, AddReminderForm, EditReminderForm, MedicineFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reminder, DAYS_CHOICES, Medicine

# Create your views here.
def home(request):
    base_template = 'pillreminder/base.html'
    if request.user.is_authenticated:
        base_template = 'pillreminder/dashboard.html'
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
        return self.render_to_response({'form': form, 'medicineFormSet': formset})

    def post(self, *args, **kwargs):
        form = AddReminderForm(self.request.POST)
        formset = MedicineFormSet(self.request.POST)
        new_reminder = 0
        if form.is_valid():
            reminder = Reminder()
            reminder.is_active = form.cleaned_data['is_active']
            reminder.days = form.cleaned_data['days']
            reminder.time = form.clean_time()
            reminder.user = self.request.user
            reminder.save()
            new_reminder = reminder

        if new_reminder and formset.is_valid():
            for med_sub in formset.cleaned_data:
                medicine = Medicine()
                medicine.name = med_sub['name']
                medicine.dosage = med_sub['dosage']
                medicine.reminder = new_reminder
                medicine.save()
            return redirect(reverse_lazy('home'))

@login_required
def reminder_details(request, pk):
    reminder = Reminder.objects.get(id=pk)
    return render(request, 'pillreminder/reminder-details.html', {'reminder': reminder})

class EditReminder(LoginRequiredMixin, UpdateView):
    model = Reminder
    template_name = 'pillreminder/edit-reminder.html'
    success_url = reverse_lazy("home")
    form_class = EditReminderForm
    def form_valid(self, form: EditReminderForm):
        reminder = form.save(commit=False)
        reminder.user = self.request.user
        reminder.time = form.clean_time()
        reminder.save()
        return super(EditReminder, self).form_valid(form)
