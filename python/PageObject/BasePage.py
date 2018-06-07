from time import  sleep

class Page():
	def __init__(self,driver):
		self.driver = driver
		self.base_url='http://localhost/phpmyadmin/index.php'
		self.timeout=10

	def open(self,url):
		url_=self.base_url+url
		print('测试的页面是 %s' %url_)
		self.driver.maximize_window()
		self.driver.get(url_)
		sleep(2)
		assert self.driver.current_url==url_,'没有打开成功 %s' %url_

	def find_element(self,*loc):
		return self.driver.find_element(*loc)
