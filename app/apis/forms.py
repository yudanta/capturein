#!/usr/bin/env python

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, Email


class RegisterForm(Form):
	username = TextField('username', [Required()])
	email = TextField('email', [Required(), Email()])
	password = TextField('password', [Required()])