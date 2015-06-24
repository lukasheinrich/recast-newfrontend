from recastfrontend.frontendconfig import config as frontendconf

DEBUG = True
SECRET_KEY = 'some_secret'
SQLALCHEMY_DATABASE_URI = frontendconf['DBPATH']