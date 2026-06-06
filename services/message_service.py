from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_NUMBER
)

client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)

def send_confirmation(name, phone, appointment_time):

    body = f"""
Hello {name},

Your appointment has been confirmed.

Appointment Time:
{appointment_time}

Thank you.
"""

    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=body,
        to=f"whatsapp:{phone}"
    )

    print(f"WhatsApp sent: {message.sid}")