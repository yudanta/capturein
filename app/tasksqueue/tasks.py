#!/usr/bin/env python

import os
from datetime import datetime

from app import app, db, celery

from app.helpers.Captureimg import Captureimg
from app.helpers.S3Helper import S3Helper

@celery.task(name='task.capture_image')
def capture_image(img_code, delete_img = False):
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
				img.captured_at = datetime.now()

				#check if config set to upload s3 then upload, if not using url direct link
				if app.config['UPLOAD_TO_S3'] == True:
					#push to amazon s3
					s3helper = S3Helper()
					upload = s3helper.upload(filename, ''.join([str(img_code), '.png']), app.config['S3_UPLOAD_DIRECTORY'])

					if upload:
						img.uploaded_to_aws = 1
						img.aws_path = unicode(''.join([app.config['S3_LOCATION'], app.config['S3_BUCKET'], '/', app.config['S3_UPLOAD_DIRECTORY'], '/', str(img_code), '.png']))	

				else:
					#set img.aws_path = local path
					img.aws_path = None
					img.local_storage = unicode(''.join([app.config['BASE_URL'], app.config['LOCAL_STORAGE'], img_code,'.png']))


				#save img object
				img.save()

				#if delete image = true then delete image from local path
				if delete_img == True and app.config['UPLOAD_TO_S3'] == True:
					try:
						os.remove(filename)
					except Exception, e:
						pass

			else:
				return False

		else:
			return False
	else:
		return False
