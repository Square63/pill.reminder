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
from main.views.UpdateAccountView import update_account_view
from main.views.ChangePasswordView import change_password_serializer
from main.views.UpcomingRemindersView import upcoming_reminders_view
from main.views.FamilyMembersView import family_members_view
from main.views.AddFamilyMember import add_family_member
from main.views.MemberView import member_view
from main.views.UpdateMemberView import member_edit
from main.views.VerificationSMSView import verification_sms_view
from main.views.VerifyCodeView import verify_code_view
from main.views.GetCallScriptView import call_script_view
from main.views.GoogleSignInView import google_signin_view

__all__ = [
    "register_view",
    "login_view",
    "reset_password_view",
    "reset_password",
    "reminders_view",
    "reminder_view",
    "user_view",
    "update_account_view",
    "change_password_serializer",
    "add_reminder_view",
    "update_reminder_view",
    "delete_reminder_view",
    "upcoming_reminders_view",
    "family_members_view",
    "add_family_member",
    "member_view",
    "member_edit",
    "verification_sms_view",
    "verify_code_view",
    "call_script_view",
    "google_signin_view"
]
