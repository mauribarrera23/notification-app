import os

from starlette.config import Config

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
__config = Config(os.path.join(os.path.dirname(ROOT_DIR), ".env"))

# General
IS_DEBUG: bool = __config("IS_DEBUG", cast=bool, default=False)
SECRET_KEY: str = __config("SECRET_KEY", cast=str, default="CHANGE_ME!!!")
# Project
APP_DESCRIPTION: str = "Cintelink application for users notifications."
APP_NAME: str = "Cintelink Notification App"
APP_VERSION: str = "0.0.1"
DOCS_URL: str = "/docs" if IS_DEBUG else None

# Database
POSTGRES_USER: str = __config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD: str = __config("POSTGRES_PASSWORD", cast=str)
POSTGRES_HOST: str = __config("POSTGRES_HOST", cast=str)
POSTGRES_PORT: str = __config("POSTGRES_PORT", cast=str)
POSTGRES_DB: str = __config("POSTGRES_DB", cast=str)
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
