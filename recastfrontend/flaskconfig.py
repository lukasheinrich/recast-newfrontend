from recastfrontend.frontendconfig import config as frontendconf
import os

DEBUG = True
SECRET_KEY = 'some_secret'
SQLALCHEMY_DATABASE_URI = frontendconf['DATABASE_URL']
