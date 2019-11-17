import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    '''
    Base config class
    '''
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 12
    SECRET_KEY = os.getenv('SECRET_KEY')
    TOKEN_EXPIRATION_DAYS = 1
    TOKEN_EXPIRATION_SECONDS = 0
    BYPASS_AUTH = False

class ProductionConfig(BaseConfig):
    """
    Production specific config
    """
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    """
    Development environment specific configuration
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3
    BYPASS_AUTH = True
