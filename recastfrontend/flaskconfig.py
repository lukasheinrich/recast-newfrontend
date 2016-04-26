from recastfrontend.frontendconfig import config as frontendconf
import os

DEBUG = True
SECRET_KEY = 'some_secret'
SQLALCHEMY_DATABASE_URI = frontendconf['DBPATH']
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
