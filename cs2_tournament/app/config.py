from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    SMTP_HOST: str = "smtp.yourmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your@email.com"
    SMTP_PASSWORD: str = "your_password"
    SMTP_FROM_EMAIL: EmailStr = "your@email.com"
    SECRET_KEY: str = "LzkdbWDBTJ7RZ7l7w5zdym_8vbwTVKRwfmuwf__nTAg"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
