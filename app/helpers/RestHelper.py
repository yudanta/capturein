#!/usr/bin/env python

from flask import Flask, json, jsonify

import time

class RestHelper():

	_response = None

	def __init__(self):
		return None

	def build_response(self, status, response_code, data, messages):
		result_formated = {
			'response_code':response_code,
			'messages':messages,
			'data':data,
		} 
		response = jsonify(result_formated)
		response.status_code = status
		return response

	def build_error_response(self, status, response_code, messages):
		error_response = {
			'response_code':response_code,
			'messages':messages,
		}
		response = jsonify(error_response)
		response.status_code = status
		return response

	@property
	def unauthorize(self):
		unauthorize_response = {
			'response_code':401,
			'mesasges':'unauthorize!'
		}
		self._response = jsonify(unauthorize_response)
		self._response.status_code = 401
		return self._response

	@property
	def forbidden(self):
		forbidden_response = {
			'response_code':403,
			'messages':'forbidden!'
		}
		self._response = jsonify(forbidden_response)
		self._response.status_code = 403
		return self._response
