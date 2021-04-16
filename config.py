from os import getenv


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_ENV")
    JSON_SORT_KEYS = getenv("JSON_SORT_KEYS")
    DEBUG = True


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_ENV")
    JWT_SECRET_KEY = getenv("SECRET_KEY")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""
    TESTING = True


config_selector = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestConfig,
}
