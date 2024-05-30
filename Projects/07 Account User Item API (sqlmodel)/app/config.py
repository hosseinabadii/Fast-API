from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_host: str
    database_url: str
    secret_key: str
    forgot_pwd_secret_key: str
    reset_password_url: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
