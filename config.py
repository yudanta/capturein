import os

BASE_URL = 'http://localhost:5000/'

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#--------------------------------------
# MongkoKit Config
#--------------------------------------
MONGODB_DATABASE = "capturein"
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 32380 #32380
MONGODB_USERNAME = "capture"
MONGODB_PASSWORD = "in-dong"

#--------------------------------------
# AWS Config #nuwira access key
#--------------------------------------
AWS_ACCESS_KEY = 'AKIAIYVFRCYTH66KSFQA'
AWS_SECRET_KEY = '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'

S3_LOCATION = 'https://s3.amazonaws.com/'
S3_UPLOAD_DIRECTORY = 'public/storage'
S3_BUCKET = 'tolong.capture.donk'
S3_ACL = 'public-read'

AWS_FULL_URL = 'https://s3.amazonaws.com/tolong.capture.donk/'

LOCAL_STORAGE = 'contents/captured_img/'

#sample token : 0bonvMYlt0KuYsxfG5ucbbevydRmkvY2

#celery config
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'