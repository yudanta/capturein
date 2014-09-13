#!/usr/bin/env python

import os

import json
from uuid import uuid4
from datetime import datetime

from bson import objectid

from werkzeug import secure_filename

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json, jsonify, Response
from app import app, db
from app.helpers.RestHelper import RestHelper
from app.helpers.HashHelper import HashHelper
from app.helpers.Captureimg import Captureimg
from app.helpers.S3Helper import S3Helper

from app.tasksqueue.tasks import capture_image

from app.apis.forms import RegisterForm, LoginForm

from app.decorators.authdecorators import *


#--------------------------------------
# Setup for blueprints
#--------------------------------------
apis = Blueprint('apis', __name__, url_prefix='/apis')

#--------------------------------------
# Users methods
#--------------------------------------
@apis.route('/')
def index():
	return RestHelper().build_response(200, 200, {}, 'Umm... hi mate, want to capture some web page?')

@apis.route('/adduser', methods=['POST'])
def adduser():
	register_form = RegisterForm(csrf_enabled=False)
	if register_form.validate_on_submit():
		cek_user = db.User.find_one({'$or':[{"username":register_form.username.data}, {"email":register_form.email.data}]})
		if cek_user:
			return RestHelper().build_response(403, 403, {}, 'username or email already exists')
		else:
			new_user = db.User()
			#print register_form.username.data
			new_user.username = unicode(register_form.username.data)
			new_user.email = unicode(register_form.email.data)
			new_user.password = unicode(HashHelper().generate_md5_hash(register_form.password.data))
			new_user.token_key = unicode(HashHelper().generate_random_string(32))
			#print new_user
			#save
			new_user.save()

			return RestHelper().build_response(200, 200, {"token_key": new_user.token_key}, 'Success add you as user :p')
	else:
		return RestHelper().build_response(412, 412, register_form.errors, 'hmm... we missing some params')

@apis.route('/auth', methods=['POST'])
def auth_user():
	login_form = LoginForm(csrf_enabled = False)
	if login_form.validate_on_submit():
		user = db.User.find_one({'$or':[{'username':login_form.username.data}, {'email':login_form.username.data}]})
		if user:
			#check password hash is valid or not
			if HashHelper().check_md5_hash(login_form.password.data, user.password):
				#renew token and save and return data
				user.token_key = unicode(HashHelper().generate_random_string(32))
				user.save()
				return RestHelper().build_response(200, 200, {"token_key": user.token_key}, 'Yay... you have been authenticate, please use your token wisely')
			else:
				return RestHelper().build_response(403, 403, {}, 'So sorry, we can\'t match your password with your email account')
		else:
			return RestHelper().build_response(403, 403, {}, 'Your username or email are not found, we can\'t authenticate, so sorry')

@apis.route('/get_image', methods=['GET'])
@token_required('GET')
def ambilindong():
	if request.args.get('img_key') != None:
		img_key = request.args.get('img_key')
		#get img key
		img = db.CaptureObj.find_one({'hashcode':img_key})
		if img:
			#return all capture obj data
			img_data = {
				'img_key' : img.hashcode,
				'url': img.url,
				'created_at': img.created_at,
				'is_captured': img.is_captured,
				'captured_at': img.captured_at,
				'status': img.status,
				'aws_path': img.aws_path,
				'filename': img.filename
			}
			return RestHelper().build_response(200, 200, img_data, 'we found it :p')
		else:
			return RestHelper().build_response(404, 404, {}, 'Image not found')
	else:
		return RestHelper().build_response(412, 412, {}, 'img_key params required')

@apis.route('/all_images', methods=['GET'])
@token_required('GET')
def gambarku():
	limit = 0
	page = 0

	try:
		if requet.args.get('limit') != None and request.args.get('limit') != '':
			limit = int(request.args.get('limit'))
	except Exception, e:
		None

	try:
		if requet.args.get('page') != None and request.args.get('page') != '':
			page = int(request.args.get('page'))
	except Exception, e:
		None

	user = db.User.find_one({'token_key':request.args.get('token')})

	#get list of images
	images = db.CaptureObj.find({'created_by':str(user._id)}, limit=limit, skip=limit*page)
	if images:
		#prepare return data
		return_data = []
		for img in images:
			new_obj = {
				'img_key' : img.hashcode,
				'url': img.url,
				'created_at': img.created_at,
				'is_captured': img.is_captured,
				'captured_at': img.captured_at,
				'status': img.status,
				'aws_path': img.aws_path,
				'filename': img.filename
			}

			return_data.append(new_obj)
		return RestHelper().build_response(200, 200, {"images":return_data}, 'We found it!')
			
	else:
		return RestHelper().build_response(404, 404, {}, 'Data not found!')

@apis.route('/capture', methods=['POST'])
@token_required('POST')
def capture_queue():
	current_user = db.User.find_one({'token_key':request.form['token']})
	if current_user:
		if request.method == 'POST' and 'url' in request.form:
			url = request.form['url']
			if url != '':
				hashed = uuid4()
				filename = ''.join([str(hashed), '.png'])
				local_storage = ''.join([app.config['LOCAL_STORAGE'], str(hashed), '.png'])

				new_obj = db.CaptureObj()
				new_obj.hashcode = unicode(hashed)
				new_obj.url = unicode(url)
				new_obj.is_captured = 0
				new_obj.status = 1
				new_obj.filename = unicode(filename)
				new_obj.local_storage = unicode(local_storage)
				new_obj.created_by = str(current_user._id)
				new_obj.captured_at = None

				#save data then call celery tasks
				new_obj.save()

				#call celery tasks
				capture_image.delay(str(hashed), True)

				return RestHelper().build_response(200, 200, {'img_key': new_obj.hashcode}, 'Success :p')
	
		else:
			return RestHelper().build_response(412, 412, {}, 'Url required!')

	else:
		return RestHelper().build_response(403, 403, {}, 'Unauthorized!')

@apis.route('/capturedong', methods=['POST'])
@token_required('POST')
def capturedong():
	current_user = db.User.find_one({'token_key':request.form['token']})
	if current_user:
		if request.method == 'POST' and 'url' in request.form:
			url = request.form['url']
			if url != '':
				hashed = uuid4()
				imgcapture = Captureimg()
				filename = ''.join([str(hashed), '.png'])
				local_storage = imgcapture.capture_img(url, hashed)
				if filename and filename != '':
					#create new capture image obj
					new_obj = db.CaptureObj()
					new_obj.hashcode = unicode(hashed)
					new_obj.url = unicode(url)
					new_obj.is_captured = 1
					new_obj.status = 1
					new_obj.filename = unicode(filename)
					new_obj.local_storage = unicode(local_storage)
					new_obj.created_by = str(current_user._id)
					new_obj.captured_at = datetime.now()

					#push to amazon s3
					s3helper = S3Helper()
					upload = s3helper.upload(filename, ''.join([str(hashed), '.png']), app.config['S3_UPLOAD_DIRECTORY'])

					if upload:
						new_obj.aws_path = unicode(''.join([app.config['S3_LOCATION'], app.config['S3_BUCKET'], '/', app.config['S3_UPLOAD_DIRECTORY'], '/', str(hashed), '.png']))

					print new_obj

					#save obj after push to amazon s3
					new_obj.save()

					return RestHelper().build_response(200, 200, {'img_key': new_obj.hashcode, 'aws_url':new_obj.aws_path}, 'Success :p')
				else:
					return RestHelper().build_response(500, 500, {}, 'Image not captured, damn')	
	
		else:
			return RestHelper().build_response(412, 412, {}, 'Url required!')

	else:
		return RestHelper().build_response(403, 403, {}, 'Unauthorized!')