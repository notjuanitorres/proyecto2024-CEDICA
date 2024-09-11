class Config(object):
    """BASE CONFIGURATION"""

    SECRET_KEY = "mysecretkey"
    TESTING = False
    DEBUG = False
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    """PRODUCTION CONFIGURATION"""


class DevelopmentConfig(Config):
    """DEVELOPMENT CONFIGURATION"""

    DEBUG = True


class TestingConfig(Config):
    """TESTING CONFIGURATION"""

    TESTING = True

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
