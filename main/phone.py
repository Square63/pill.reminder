from django.conf import settings
from twilio.rest import Client

def make_phone_call(phone_number, reminder_type_id):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    call = client.calls.create(
        url=f"https://pillreminder.square63.net/api/{reminder_type_id}/get-call-script",
        to=phone_number,
        from_="+15102395727"
    )

    return call.sid
