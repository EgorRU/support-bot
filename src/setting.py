"""
Конфигурация приложения на pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot


class Settings(BaseSettings):
    """
    Класс для хранения и валидации настроек приложения.
    """

    # Настройки бота
    BOT_TOKEN: str
    GROUP_ID: int
    
    # Настройки базы данных
    DATABASE_URL: str = "sqlite+aiosqlite:///database.db"

    class Config(SettingsConfigDict):
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

bot = Bot(settings.BOT_TOKEN)