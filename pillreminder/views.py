from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, UserUpdateForm, AddReminderForm, EditReminderForm, EditMedicineForm, MedicineFormSet, EditMedicineFormSet, ProfilePictureForm, ContactForm
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reminder, DAYS_CHOICES, Medicine, UserMethods as User, ProfilePicture
from django.core.mail import send_mail

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
    user = User.objects.get(id=request.user.id)
    base_template = 'pillreminder/base.html'
    if request.user.is_authenticated:
        base_template = 'pillreminder/dashboard.html'
    return render(request, 'pillreminder/profile.html', {'base_template': base_template, 'user': user})

class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'pillreminder/profile-edit.html'
    success_url = reverse_lazy("profile")
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user
    def get(self, *args, **kwargs):
        form = UserUpdateForm(instance=self.request.user)
        try:
            picture = ProfilePicture.objects.get(user_id=1)
        except ProfilePicture.DoesNotExist:
            picture = None
        picform = ProfilePictureForm(instance=picture)
        return self.render_to_response({'form': form, 'picform': picform})
    def post(self, *args, **kwargs):
        form = UserUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user)
        try:
            picture = ProfilePicture.objects.get(user_id=1)
        except ProfilePicture.DoesNotExist:
            picture = None
        picform = ProfilePictureForm(self.request.POST, self.request.FILES, instance=picture)
        if form.is_valid() and picform.is_valid():
            form.save()
            if picture:
                picture.image = picform.cleaned_data['image']
                picture.user = self.request.user
                picture.save()
            else:
                picture = ProfilePicture()
                picture.image = picform.cleaned_data['image']
                picture.user = self.request.user
                picture.save()
        messages.success(self.request, 'Profile has been updated.')
        return redirect(reverse_lazy('profile'))

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
                try:
                    medicine = Medicine.objects.get(id=med_sub['id'])
                except Medicine.DoesNotExist:
                    medicine = Medicine()
                medicine.name = med_sub['name']
                medicine.dosage = med_sub['dosage']
                medicine.reminder = reminder
                if med_sub.get('delete'):
                    medicine.delete()
                else:
                    medicine.save()
            messages.success(self.request, 'The reminder has been updated.')
            return redirect(reverse_lazy('home'))
        else:
            return self.render_to_response({'form': form})

def contact(request):
    base_template = 'pillreminder/base.html'
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['name']
            message = form.cleaned_data['message']
            print(form.cleaned_data)
            send_mail(
                subject=subject,
                message=message,
                from_email='pillreminder@square63.com',
                recipient_list=["raza1778@gmail.com"],
                fail_silently=False
            )
            messages.success(request, 'Thank you contacting us.')
            return redirect(reverse_lazy('contact'))

    return render(request, 'pillreminder/contact.html', {'base_template': base_template, 'form': form})
