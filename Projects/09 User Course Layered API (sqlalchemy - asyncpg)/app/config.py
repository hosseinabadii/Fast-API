from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    password_schemes: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire: int
    jwt_refresh_token_expire: int
    mail_username: str
    mail_password: str
    mail_port: int
    mail_server: str
    mail_from: EmailStr
    url_safe_secret_key: str
    url_safe_token_expire: int
    domain: str
    redis_url: str
    redis_jti_expire: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
