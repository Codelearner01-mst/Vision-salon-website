import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
       SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
       MAIL_SERVER = os.environ.get("MAIL_SERVER","smtp.googlemail.com")
       MAIL_PORT = os.environ.get("MAIL_PORT", 587)
       MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
       MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
       MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
       VISION_MAIL_SENDER = "vision salon <kwabenap603@gmail.com>"
       SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
       SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or  'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
       DEBUG = True

class TestingConfig(Config):
       SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or 'sqlite:///data-test.sqlite'
       TESTING= True
    
class ProductionConfig(Config):
       SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URL") or 'sqlite:///data.sqlite'

config = {
       "default":DevelopmentConfig,
       "development":DevelopmentConfig,
       "testing":TestingConfig,
       "production":ProductionConfig,

}