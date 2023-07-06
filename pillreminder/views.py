from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return render(request, 'pillreminder/home.html')

class SignUp(CreateView):
    model = User
    template_name = 'pillreminder/signup.html'
    success_url = reverse_lazy("login")
    form_class = SignUpForm

@login_required
def profile(request):
    return render(request, 'pillreminder/profile.html')

class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'pillreminder/profile-edit.html'
    success_url = reverse_lazy("profile")
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user
