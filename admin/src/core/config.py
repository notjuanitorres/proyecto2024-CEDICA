import os
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """BASE CONFIGURATION"""

    SECRET_KEY = "mysecretkey"
    TESTING = False
    DEBUG = False
    SESSION_TYPE = "filesystem"
    SEED_ON_STARTUP = False


class ProductionConfig(Config):
    """PRODUCTION CONFIGURATION"""

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


class DevelopmentConfig(Config):
    """DEVELOPMENT CONFIGURATION"""

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
