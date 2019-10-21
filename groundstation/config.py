import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	'''
	Base config class
	'''
	DEBUG = True
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

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
