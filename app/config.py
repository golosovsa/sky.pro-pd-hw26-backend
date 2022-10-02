import base64
import os
from urllib.parse import quote_plus
from pathlib import Path
from typing import Type

BASE_DIR = Path.cwd()


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'rZwVQ2Cpz7R89Bzj')
    JWT_ALGORITHM = "HS256"
    JSON_AS_ASCII = False

    ITEMS_PER_PAGE = 12

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130

    PWD_HASH_SALT = base64.b64decode("salt")
    PWD_HASH_ITERATIONS = 100_000

    RESTX_JSON = {
        'ensure_ascii': False,
    }


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + (BASE_DIR / "app.db").as_posix()
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://" \
                              f"{os.getenv('DATABASE_USER', default='DATABASE_USER')}:" \
                              f"{quote_plus(os.getenv('DATABASE_PASSWORD', default='DATABASE_PASSWORD'))}@" \
                              f"{os.getenv('DATABASE_HOST', default='DATABASE_HOST')}:5432/" \
                              f"{os.getenv('DATABASE_NAME', default='DATABASE_NAME')}"

class ConfigFactory:
    flask_env = "development"

    @classmethod
    def get_config(cls) -> Type[BaseConfig]:
        cls.flask_env = os.getenv('FLASK_ENV')
        if cls.flask_env == 'development':
            print("Development config")
            return DevelopmentConfig
        elif cls.flask_env == 'production':
            print("Production config")
            return ProductionConfig
        elif cls.flask_env == 'testing':
            print("Testing config")
            return TestingConfig
        raise NotImplementedError


config = ConfigFactory.get_config()
