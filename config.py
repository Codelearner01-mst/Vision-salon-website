import os

class Config():
       SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
       SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
       SQLALCHEMY_DATABASE_URI = os.environ.get("")
       DEBUG = True

class TestingConfig(Config):
       SQLALCHEMY_DATABASE_URI = os.environ.get("")
       TESTING= True
    
class ProductionConfig(Config):
       SQLALCHEMY_DATABASE_URI = os.environ.get("")

config = {
       "default":DevelopmentConfig,
       "development":DevelopmentConfig,
       "testing":TestingConfig,
       "production":ProductionConfig,

}