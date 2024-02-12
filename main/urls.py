from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from main.views import (
    register_view,
    login_view,
    reminders_view,
    reminder_view,
    user_view,
    user_update_view,
    add_reminder_view
)

urlpatterns = [
    path('auth/signup', register_view, name='signup'),
    path('auth/signin', login_view, name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user', user_view, name='user'),
    path('user/update', user_update_view, name='user_update'),
    path('reminders', reminders_view, name='user_reminders'),
    path('reminder/<int:pk>', reminder_view, name='user_reminder'),
    path('add/reminder', add_reminder_view, name='add_reminder'),
]
