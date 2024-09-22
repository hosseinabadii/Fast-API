from pathlib import Path

from config import settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from utils import create_url_safe_token

BASE_DIR = Path(__file__).resolve().parent


mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM=settings.mail_from,
    MAIL_FROM_NAME="FastAPI",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=BASE_DIR / "templates/emails",
)

fastmail = FastMail(config=mail_config)


def create_message(recipients: list[EmailStr], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
    )
    return message


async def send_email(message: MessageSchema):
    await fastmail.send_message(message)


async def send_verification_email(email):
    url_safe_token = create_url_safe_token({"email": email}, salt="verification")
    url = f"{settings.domain}/account/verify-account?token={url_safe_token}"
    body = f"""
    <html>
        <body>
            <h1>Verify your email</h1>
            <p>Click on the link below</p>
            <a href="{url}">Click here</a>
        </body>
    </html>
    """
    message = create_message(recipients=[email], subject="Verify your email", body=body)
    await send_email(message)


async def send_reset_password_email(email):
    url_safe_token = create_url_safe_token({"email": email}, salt="reset-password")
    url = f"{settings.domain}/account/password-reset-confirm?token={url_safe_token}"
    body = f"""
    <html>
        <body>
            <h1>Reset Your Password</h1>
            <p>Click on the link below</p>
            <a href="{url}">Click here</a>
        </body>
    </html>
    """
    message = create_message(
        recipients=[email], subject="Reset Your Password", body=body
    )
    await send_email(message)
