import os
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """BASE CONFIGURATION

    Attributes:
        SECRET_KEY: str
        TESTING: bool
        DEBUG: bool
        SESSION_TYPE: str
        SEED_ON_STARTUP: bool
    """

    SECRET_KEY = "mysecretkey"
    TESTING = False
    DEBUG = False
    SESSION_TYPE = "filesystem"
    SEED_ON_STARTUP = False
    CKEDITOR_PKG_TYPE = "basic"
    CORS_ORIGINS = ["http://localhost:5173"]


class ProductionConfig(Config):
    """PRODUCTION CONFIGURATION

    Attributes:
        MINIO_SERVER: str
        MINIO_ACCESS_KEY: str
        MINIO_SECRET_KEY: str
        MINIO_SECURE: bool
        SQLALCHEMY_DATABASE_URI: str
        SQLALCHEMY_ENGINE_OPTIONS: Dict
        SEED_ON_STARTUP: bool
    """

    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }
    SEED_ON_STARTUP = True
    CORS_ORIGINS = Config.CORS_ORIGINS + ["https://admin-grupo19.proyecto2024.linti.unlp.edu.ar:5173"]


class DevelopmentConfig(Config):
    """DEVELOPMENT CONFIGURATION

    Attributes:
        MINIO_SERVER: str
        MINIO_ACCESS_KEY: str
        MINIO_SECRET_KEY: str
        MINIO_SECURE: bool
        SQLALCHEMY_DATABASE_URI: str
    """

    MINIO_SERVER = os.getenv("MINIO_SERVER_DEVELOPMENT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY_DEVELOPMENT")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY_DEVELOPMENT")
    MINIO_SECURE = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI_DEVELOPMENT")


class TestingConfig(Config):
    """TESTING CONFIGURATION"""

    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
