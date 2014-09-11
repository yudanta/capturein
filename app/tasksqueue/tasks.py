#!/usr/bin/env python

from app import app, db, celery

from app.helpers.Captureimg import Captureimg
from app.helpers.S3Helper import S3Helper

@celery.task(name='task.capture_image')
def capture_image(img_code):
	#get img data from img_code and then capture and send it to amazon s3
	if img_code != '':
		img = db.CaptureObj.find_one({'hashcode':img_code})
		if img:
			#capture image 
			imgcapture = Captureimg()
			filename = imgcapture.capture_img(img.url, img_code)
			if filename:
				#update aws path
				img.is_captured = 1

				#push to amazon s3
				s3helper = S3Helper()
				upload = s3helper.upload(filename, ''.join([str(img_code), '.png']), app.config['S3_UPLOAD_DIRECTORY'])

				if upload:
					img.aws_path = unicode(''.join([app.config['S3_LOCATION'], app.config['S3_BUCKET'], '/', app.config['S3_UPLOAD_DIRECTORY'], '/', str(img_code), '.png']))

				#save obj after push to amazon s3
				img.save()

			else:
				return False

		else:
			return False
	else:
		return False
