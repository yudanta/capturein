#!/usr/bin/env python

from app import app

from selenium import webdriver

from uuid import uuid4

class Captureimg():

	url = ''
	name = ''

	def __init__(self):
		return None

	def capture_img(self, url, hashed):
		if url != '' or url != None:
			self.url = url

		if self.url != '':
			#go capture
			self.name = ''.join([app.config['LOCAL_STORAGE'], str(hashed), '.png'])
			browser = webdriver.Firefox()
			browser.get(self.url)
			browser.save_screenshot(self.name)
			browser.quit()
			return self.name
		else:
			return False