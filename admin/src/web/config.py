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


class ProductionConfig(Config):
    """PRODUCTION CONFIGURATION"""
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    """DEVELOPMENT CONFIGURATION"""
    DBUSER = os.getenv("DBUSER")
    DBPASS = os.getenv("DBPASS")
    DBHOST = "localhost"
    DBPORT = "5432"
    print(DBPORT)
    print(DBHOST)
    DBNAME = os.getenv("DBNAME")
    print(DBNAME)
    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"


class TestingConfig(Config):
    """TESTING CONFIGURATION"""

    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
