# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

def browser(boolean):
	options = Options()
	# driver = webdriver.PhantomJS()
	# driver = Firefox(executable_path='geckodriver', firefox_options=options)
	if boolean == True:
		print('-------------------->无头模式<--------------------')
		options.add_argument('--disable-gpu')
		options.add_argument('--headless')
		options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
		driver = webdriver.Chrome(options=options)
		return driver
	else:
		print('-------------------->有头模式<--------------------')
		# 自动下载目录，禁止下载弹窗
		prefs = {'profile.default_content_settings.popups': 0,'download.default_directory': 'F:\\WorkPlace\\Python\\python\\AutoBaikeProject\\website\\test_data\imgs'}
		options.add_experimental_option('prefs', prefs)
		options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
		driver = webdriver.Chrome(options=options)
		return driver



