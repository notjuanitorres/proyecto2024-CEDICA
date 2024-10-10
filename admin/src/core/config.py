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
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SEED_ON_STARTUP = True


class DevelopmentConfig(Config):
    """DEVELOPMENT CONFIGURATION"""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI_DEVELOPMENT")


class TestingConfig(Config):
    """TESTING CONFIGURATION"""

    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
