import os
from dataclasses import dataclass, field

from environs import Env

from app.config.logger import LoggerConfig

env = Env()
env.read_env()


# Настройки базы данных
@dataclass
class DatabaseConfig:
    user: str = os.environ.get("DB_USER")
    password: str = os.environ.get("DB_PASSWORD")
    host: str = os.environ.get("DEV_DB_HOST")
    port: int = 5432
    name: str = os.environ.get("DB_NAME")

@dataclass
class TokenConfig:
    TOKEN: str = os.environ.get("TOKEN")

# Создание базового config класса
@dataclass
class BaseConfig:
    token: TokenConfig = field(default_factory=TokenConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logger: LoggerConfig = field(default_factory=LoggerConfig)


# Настройки конфигурации для продакшена
@dataclass
class ProdConfig(BaseConfig):
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig(
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        name=os.environ.get("DB_NAME")))


# Используем конфигурацию production если передана соответствующая переменная
# устанавливается обычно в файле Docker при сборке контейнера
if os.environ.get("FASTAPI_ENV") == "production":
    config = ProdConfig()
else:
    config = BaseConfig()
