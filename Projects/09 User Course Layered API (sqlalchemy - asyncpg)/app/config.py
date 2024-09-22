from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    password_schemes: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    mail_username: str
    mail_password: str
    mail_port: int
    mail_server: str
    mail_from: EmailStr
    token_expire: int
    domain: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
