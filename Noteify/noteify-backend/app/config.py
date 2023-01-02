from pydantic import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "somethingiforgot"
    database_name: str = "fastapi"
    database_username: str = "postgres"
    supported_subcodes: dict = {"yettoconfigure": "some code"}
    regmod_emails: list = ["abcd.gmail.com", "efgh.ymail.com"]
    secret_key: str = "idontknowthatyetbutilltry"
    encryption_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = "app{}.env".format(os.sep)
        env_file_encoding = "utf-8"


settings = Settings()
