#!/usr/bin/env python

from datetime import datetime

from functools import wraps
from flask import g, request, redirect, url_for

from app import db

from app.helpers.RestHelper import RestHelper

def token_required(method):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			#check token is valid or not
			token = ''
			if method == 'POST' and 'token' in request.form:
				token = request.form['token']
			if method == 'GET' and request.args.get('token') != None:
				token = request.args.get('token')

			if token == '' or token == None:
				return RestHelper().build_response(412, 412, {}, 'Token required')
			else:
				#check
				user = db.User.find_one({"token_key":token})
				if user:
					return f(*args, **kwargs)
				else:
					return RestHelper().build_response(403, 403, {}, 'Unauthorized!')

		return decorated_function
	return decorator