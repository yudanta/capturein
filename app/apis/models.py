#!/usr/bin/env python

from datetime import datetime

from flask.ext.mongokit import MongoKit, Document

from app import db

class CaptureObj(Document):
	__database__ = 'capturein'
	__collection__ = 'captures'

	structure = {
		'hashcode' : unicode,
		'url': unicode,
		'created_at': datetime,
		'is_captured': int,
		'captured_at': datetime,
		'updated_at': datetime,
		'status': int,
		'aws_path': unicode,
		'filename': unicode,
		'local_storage': unicode,
		'created_by': basestring
	}

	required_fields = ['hashcode', 'url', 'created_at', 'is_captured', 'status', 'filename', 'created_by']

	default_values = {
		'created_at': datetime.now(),
		'is_captured': 0,
		'status': 1
	}

	use_dot_notation = True


class User(Document):
	__database__ = 'capturein'
	__collection__ = 'users'

	structure = {
		'username': unicode,
		'email': unicode,
		'password': unicode,
		'token_key': unicode,
		'status': int,
		'created_at': datetime,
		'updated_at': datetime
	}

	required_fields = ['email', 'username', 'password', 'status', 'created_at']

	default_values = {
		'created_at': datetime.now(),
		'status': 1
	}

	use_dot_notation = True