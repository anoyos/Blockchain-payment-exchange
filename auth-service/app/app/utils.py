from pathlib import Path

from api_contrib.core.email import send_email

from app.core.config import settings


def send_reset_password_email(email_to: str, token: str) -> None:
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()

    send_email(
        settings,
        email_to=email_to,
        subject_template="[Bullflag] Verify password change",
        html_template=template_str,
        environment={
            "host": settings.DOMAIN,
            "token": token
        }
    )


def send_change_password_notification(email_to: str, username: str) -> None:
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "change_password_notification.html") as f:
        template_str = f.read()

    send_email(
        settings,
        email_to=email_to,
        subject_template="[Bullflag] Password changed",
        html_template=template_str,
        environment={
            "host": settings.DOMAIN,
            "username": username
        }
    )


def send_new_account_email(email_to: str, username: str, token: str) -> None:
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "signup.html") as f:
        template_str = f.read()

    send_email(
        settings,
        email_to=email_to,
        subject_template="[Bullflag] Verify your e-mail",
        html_template=template_str,
        environment={
            "host": settings.DOMAIN,
            "token": token,
            "username": username,
        }
    )
