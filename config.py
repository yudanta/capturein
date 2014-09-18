import os

BASE_URL = 'http://localhost:5000/'

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#--------------------------------------
# MongkoKit Config
#--------------------------------------
MONGODB_DATABASE = "capturein"
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017 #32380
MONGODB_USERNAME = None #"capture"
MONGODB_PASSWORD = None #"in-dong"

UPLOAD_TO_S3 = False

#--------------------------------------
# AWS Config #nuwira access key
#--------------------------------------
AWS_ACCESS_KEY = '<aws access key>'
AWS_SECRET_KEY = '<aws secret key>'

S3_LOCATION = 'https://s3.amazonaws.com/'
S3_UPLOAD_DIRECTORY = '<your aws target upload dir>'
S3_BUCKET = '<your aws bucket>'
S3_ACL = 'public-read'

AWS_FULL_URL = '<your aws full url>'

LOCAL_STORAGE = 'storage/public/images/'

#sample token : 0bonvMYlt0KuYsxfG5ucbbevydRmkvY2

#celery config
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'