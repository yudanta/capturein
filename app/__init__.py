#!/usr/bin/env python

import os
import time

from flask import Flask, render_template, send_from_directory, Response, request, render_template, redirect, url_for
from flask.ext.celery3 import make_celery
from flask.ext.mongokit import MongoKit, Document

from app.helpers.RestHelper import RestHelper

#--------------------------------------
# App config
#--------------------------------------
app = Flask(__name__, instance_relative_config=True)

#load local config
app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

#--------------------------------------
# setup for celery
#--------------------------------------

celery = make_celery(app)

#--------------------------------------
# setup for mongokit
#--------------------------------------
db = MongoKit(app)

from app.apis.models import CaptureObj, User

#register to db
db.register([CaptureObj, User])

#--------------------------------------
# setup for blueprints
#--------------------------------------
from app.apis import apis

app.register_blueprint(apis)

#--------------------------------------
# default controler
#--------------------------------------

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
	#return render_template('404.html'), 404
	return RestHelper().build_response(404, 404, {}, 'API End point not found!')

@app.errorhandler(405)
def method_not_allowed(e):
	return RestHelper().build_response(405, 405, {}, "Method not method not allowed!")

@app.route('/', methods=['GET'])
def index():
	return RestHelper().build_response(200, 200, {}, 'Hi mate... ')
	
application = app