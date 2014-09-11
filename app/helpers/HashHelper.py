#!/usr/bin/env python

import string
import random

import hashlib

class HashHelper():

	def __init__(self):
		return None

	def generate_random_string(self, length = 16):
		chars = string.ascii_letters + string.digits
		gen = ''.join(random.choice(chars) for x in range(length))
		return gen

	def generate_md5_hash(self, plain):
		return hashlib.md5(plain).hexdigest()

	def check_md5_hash(self, plain, hashed):
		if hashlib.md5(plain).hexdigest() == hashed:
			return True
		else:
			return False

