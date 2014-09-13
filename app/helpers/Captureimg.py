#!/usr/bin/env python

from app import app

from selenium import webdriver

#adding xvfbwrapper if needed for headless  server
#from xvfbwrapper import Xvfb

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
			#adding xvfb wrapper for headless server, just on comment it with import also
			#vdisplay = Xvfb()  
			#vdisplay.start()

			#go capture
			self.name = ''.join([app.config['LOCAL_STORAGE'], str(hashed), '.png'])
			browser = webdriver.Firefox()
			browser.get(self.url)
			browser.save_screenshot(self.name)
			browser.quit()
			
			#close vdisplay from xvfbwrapper
			#vdisplay.stop()

			return self.name

		else:
			return False