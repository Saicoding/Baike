from time import sleep


class Page():
	def __init__(self, driver, options):
		self.options = options
		self.driver = driver
		self.base_url = options['base_url']
		self.timeout = 10

	def _open(self):
		url_ = self.base_url+ self.options['url']
		self.driver.maximize_window()
		self.driver.get(url_)
		sleep(2)
		assert self.driver.current_url == url_, '没有打开成功 %s' % url_

	def find_element(self, *loc):
		return self.driver.find_element(*loc)
