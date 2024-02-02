from django.urls import path
from main.views import (
    register_view,
    login_view,
    reminders_view
)

urlpatterns = [
    path('auth/signup', register_view, name='signup'),
    path('auth/signin', login_view, name='token_obtain_pair'),
    path('reminders', reminders_view, name='user_reminders')
]
