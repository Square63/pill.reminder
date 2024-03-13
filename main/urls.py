from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from main.views import (
    register_view,
    login_view,
    reset_password_view,
    reset_password,
    reminders_view,
    reminder_view,
    user_view,
    update_account_view,
    change_password_serializer,
    add_reminder_view,
    update_reminder_view,
    delete_reminder_view,
    upcoming_reminders_view,
    family_members_view,
    add_family_member,
    member_view,
    member_edit,
    verification_sms_view,
    verify_code_view,
    call_script_view
)

urlpatterns = [
    path('auth/signup', register_view, name='signup'),
    path('auth/signin', login_view, name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('send-reset-link', reset_password_view, name='api-send-reset-link'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='api-reset-password'),
    path('user', user_view, name='user'),
    path('user/update-account', update_account_view, name='account_update'),
    path('user/update-password', change_password_serializer, name='password_update'),
    path('user/upcoming/reminders', upcoming_reminders_view, name='upcoming_reminders'),
    path('reminders', reminders_view, name='user_reminders'),
    path('reminder/<int:pk>', reminder_view, name='user_reminder'),
    path('reminder/<int:pk>/update', update_reminder_view, name='update_reminder'),
    path('reminder/<int:pk>/delete', delete_reminder_view, name='delete_reminder'),
    path('add/reminder', add_reminder_view, name='add_reminder'),
    path('get-family-members', family_members_view, name='family_members_view'),
    path('family/add-member', add_family_member, name='add-family-member'),
    path('member/<int:pk>', member_view, name='member-view'),
    path('member/<int:pk>/edit', member_edit, name='member-edit'),
    path('send-verification-sms/<int:pk>', verification_sms_view, name='send-verification-sms'),
    path('verify-code/<int:pk>', verify_code_view, name='verify-code'),
    path('<int:pk>/get-call-script', call_script_view, name='call=script')
]
