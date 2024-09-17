from os import environ


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
    DBUSER = "postgres"
    DBPASS = "postgres"
    DBHOST = "localhost"
    DBPORT = "5432"
    DBNAME = "grupo 19"
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
