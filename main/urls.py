from django.urls import path
from main.views import (
    register_view,
    login_view
)

urlpatterns = [
    path('auth/signup', register_view, name='signup'),
    path('auth/login', login_view, name='token_obtain_pair'),
    # path('profile', views.profile, name='profile'),
    # path('profile/<pk>/edit', views.ProfileEdit.as_view(), name='profile-edit'),
    # path('add-reminder', views.AddReminder.as_view(), name='add-reminder'),
    # path('reminder/<pk>', views.reminder_details, name='reminder'),
    # path('reminder/<pk>/edit', views.EditReminder.as_view(), name='reminder-edit'),
    # path('reminder/<pk>/delete', views.DeleteReminder.as_view(), name='reminder-delete'),
    # path('contact', views.contact, name='contact'),
]
