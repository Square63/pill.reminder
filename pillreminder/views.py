from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm

# Create your views here.
def home(request):
    return render(request, 'pillreminder/home.html')

class SignUp(CreateView):
    model = User
    template_name = 'pillreminder/signup.html'
    success_url = reverse_lazy("login")
    form_class = SignUpForm
