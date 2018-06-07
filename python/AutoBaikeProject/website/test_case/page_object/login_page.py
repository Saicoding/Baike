from base_page import *


class LoginPage(Page):

	def type_username(self, username):
		self.find_element(*self.options['username_loc']).clear()
		self.find_element(*self.options['username_loc']).send_keys(username)

	def type_password(self, password):
		self.find_element(*self.options['password_loc']).clear()
		self.find_element(*self.options['password_loc']).send_keys(password)

	def type_submit(self):
		self.find_element(*self.options['submit_loc']).click()

	def login_pass_hint(self):
		return self.find_element(*self.options['pass_loc']).text

	def login_fail_hint(self):
		return self.find_element(*self.options['fail_loc']).text

	def login_action(self):
		self._open()
		self.type_username(self.options['username'])
		self.type_password(self.options['password'])
		self.type_submit()






