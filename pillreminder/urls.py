from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.SignUp.as_view(), name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile/<pk>/edit', views.ProfileEdit.as_view(), name='profile-edit')
]
