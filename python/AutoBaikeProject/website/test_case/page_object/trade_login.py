from login_page import *


class LoginBaike(LoginPage):
	def trade(self):
		self.find_element(*self.options['trade_loc']).click()

	def login_action(self):
		self._open()
		self.trade()
		self.type_username(self.options['username'])
		self.type_password(self.options['password'])
		self.type_submit()
		sleep(3)



