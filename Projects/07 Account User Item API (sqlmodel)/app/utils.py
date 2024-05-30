from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def send_fake_email(email: str) -> None:
    """This function just print the email to the console!"""
    print("-" * 50)
    print(f"You reset password link:\n{email}")
    print("-" * 50)
