from recastfrontend.frontendconfig import config as frontendconf

BROKER_URL = 'redis://' + frontendconf['HOSTNAME']
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = frontendconf['HOSTNAME']
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0
CELERY_TRACK_STARTED = True