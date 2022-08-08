# Download the helper library from https://www.twilio.com/docs/python/install

from twilio.rest import Client

from app.core.config import settings


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_verification_message(user_phone: str, verify_token: str):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verify_link = f'https://{settings.DOMAIN}{settings.API_V1_STR}/profile/verify?token={verify_token}'
    message = client.messages \
        .create(
            body=f"To confirm phone, click to link {verify_link}",
            from_='+19543290413',
            to=user_phone
        )
    return message.sid
