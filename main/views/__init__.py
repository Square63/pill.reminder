from main.views.RegisterView import register_view
from main.views.LoginView import login_view
from main.views.ResetPasswordView import reset_password_view
from main.views.ResetPassword import reset_password
from main.views.RemindersView import reminders_view
from main.views.ReminderView import reminder_view
from main.views.AddReminderView import add_reminder_view
from main.views.UpdateReminderView import update_reminder_view
from main.views.DeleteReminderView import delete_reminder_view
from main.views.UserView import user_view
from main.views.UserUpdateView import user_update_view
from main.views.UpcomingRemindersView import upcoming_reminders_view

__all__ = [
    "register_view",
    "login_view",
    "reset_password_view",
    "reset_password",
    "reminders_view",
    "reminder_view",
    "user_view",
    "user_update_view",
    "add_reminder_view",
    "update_reminder_view",
    "delete_reminder_view",
    "upcoming_reminders_view"
]
