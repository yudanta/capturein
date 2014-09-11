#!/usr/bin/env python 
import os.path
import sys

import boto
from werkzeug import secure_filename
from app import app

class S3Helper():
	
	messages = ""
	errors = ""
	tags = ""

	s3location = app.config['S3_LOCATION']
	s3bucket = app.config['S3_BUCKET']

	s3directory = app.config['S3_UPLOAD_DIRECTORY']
	s3acl = app.config['S3_ACL']
	conn = None
	bucket = None
	filename = ""
	file_ext = ""
	dest_filename = ""

	def __init__(self, *args, **kwargs):
		if 's3_location' in kwargs:
			self.s3location = kwargs['s3location']
		if 's3bucket' in kwargs:
			self.s3bucket = kwargs['s3bucket']
		if 's3acl' in kwargs:
			self.s3acl = kwargs['s3acl']

		#create connection 
		self.conn = boto.connect_s3(app.config['AWS_ACCESS_KEY'], app.config['AWS_SECRET_KEY'])
		self.bucket = self.conn.get_bucket(self.s3bucket)

		return None

	def upload(self, upload_file, filename, upload_dir, *args, **kwargs):
		if 's3_location' in kwargs:
			self.s3location = kwargs['s3location']
		if 's3bucket' in kwargs:
			self.s3bucket = kwargs['s3bucket']
		if 's3acl' in kwargs:
			self.s3acl = kwargs['s3acl']

		#create connection if not exists
		if self.conn == None:
			self.conn = boto.connect_s3(app.config['S3_KEY'], app.config['S3_SECRET'])
			self.bucket = conn.get_bucket(self.s3bucket)

		newS3Object = self.bucket.new_key('/'.join([self.s3directory, filename]))
		newS3Object.set_contents_from_filename(upload_file)

		#set acl
		newS3Object.set_acl(self.s3acl)

		return True

	def upload_dir(self, source_dir, upload_dir, *args, **kwargs):
		#print upload_dir
		if 's3location' in kwargs:
			self.s3location = kwargs['s3location']
		if 's3bucket' in kwargs:
			self.s3bucket = kwargs['s3bucket']
		if 's3acl' in kwargs:
			self.s3acl = kwargs['s3acl']

		#create connection if not exists
		if self.conn == None:
			self.conn = boto.connect_s3(app.config['S3_KEY', app.config['S3_SECRET']])
			self.bucket = conn.get_bucket(self.s3bucket)

		#prep dir and file inside
		upload_filenames = []
		for (source_dir, dirname, filename) in os.walk(source_dir):
			upload_filenames.extend(filename)
			break

		#uploads
		'''
		for filename in upload_filenames:
			source_path = os.path.join(source_dir + filename)
			dest_path = '/'.join([self.s3directory, upload_dir, filename])
			print dest_path

			filesize = os.path.getsize(source_path)

			#create multipart file upload
			mp = self.bucket.initiate_multipart_upload(dest_path)
			fp = open(source_path, 'rb')
			fp_num = 0

			while (fp.tell() < filesize):
				fp_num += 1
				mp.upload_part_from_file(fp, fp_num)

		'''
		for filename in upload_filenames:
			source_path = os.path.join(source_dir + filename)
			dest_path = '/'.join([self.s3directory, upload_dir, filename])
			#add new object and uploads

			newS3Object = self.bucket.new_key(dest_path)
			#logging
			#print '/'.join([self.s3directory, dest_path])
			newS3Object.set_contents_from_filename(source_path)
			#set acl
			newS3Object.set_acl(self.s3acl)

		return True


	def set_messages(self, messages):
		self.messages = messages

	def set_errors(self, errors):
		self.errors = errors

	def set_tags(self, tags):
		self.tags = tags

	def get_messages(self):
		return self.messages

	def get_errors(self):
		return self.errors

	def get_tags(self):
		return self.tags