import unittest
from driver import *


class StartEnd(unittest.TestCase):
	headless = False
	def setUp(self):
		self.driver = browser(self.headless)
		self.driver.implicitly_wait(8)
		self.driver.maximize_window()

	def tearDown(self):
		try:
			self.driver.quit()
		except ConnectionRefusedError as e:
			print(e)

