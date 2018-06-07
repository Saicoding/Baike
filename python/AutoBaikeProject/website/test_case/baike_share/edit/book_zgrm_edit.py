from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from time import sleep


class Bookzgrm():
	def __init__(self, driver):
		self.driver = driver

	def go_to_detal_page(self, url):
		self.driver.get(url)

	# 得到百科创建的标题，基本信息，内容简介
	def get_result(self):
		# 实例化BasicBar对象
		basic_bar = BasicBar()
		is_true = True
		while True:
			try:
				# 等待跳转输入框出现
				WebDriverWait(self.driver, 15, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'dir-con')))
			except:
				is_true = False
			finally:
				if is_true == False:
					self.driver.refresh()
				else:
					break
		# 获取书名
		title = self.driver.find_element_by_css_selector('.book-title > span:nth-child(2)').get_attribute('title')
		primitive_title = title
		title = basic_bar.trade_title(title)
		# 获取基本信息栏
		basic_bar = BasicBar()
		elements = self.driver.find_elements_by_css_selector('.book-det-list > ul >li')
		for el in elements:
			basic_bar.trade(el.text)  # 处理字符串，如果是空选项就去除

		bar = basic_bar.get_basic_str()  # 基本信息栏

		# 获取作者
		author = basic_bar.zuozhe.split('作者：')[1]
		author = re.sub(r'(编著)|(主编)', '', author)
		author = author.replace('著', '')
		author = author.replace('编', '')

		# 获取内容
		content = self.driver.find_elements_by_css_selector('.info-con-text > p')[0].text  # 内容

		# 获取时间
		time = basic_bar.chubanshijian
		time = time[5:9]

		# 获取当前url
		url = self.driver.current_url

		# 获取作者简介
		author_info = self.driver.find_elements_by_css_selector('.info-con-text > p')[1].text
		author_info = re.sub('(https|http):.*(com|cn|de)', '', author_info)

		# 获取目录内容
		directory = self.driver.find_elements_by_css_selector(
			'#textbook-con > div.textbook-right.fl > div.directory > div:nth-child(2)')[0].text
		directory = re.sub('(https|http):.*(com|cn|de)', '', directory)

		# 获取下载连接
		down_url = self.driver.find_element_by_css_selector(
			'#textbook-con > div.textbook-left.fl > div.book-transform > p > a').get_attribute('href')

		return {'title': title, 'bar': bar, 'author': author, 'content': content, 'time': time, 'url': url,
		        'author_info': author_info, 'directory': directory, 'down_url': down_url,
		        'primitive_title': primitive_title}


class BasicBar():
	def __init__(self):
		self.zuozhe = ""  # 作者
		self.shuhao = ""  # 书号
		self.dingjia = ""  # 定价
		self.zishu = ""  # 字数
		self.yinci = ""  # 印次
		self.kaiben = ""  # 开本
		self.chubanshijian = ""  # 出版时间
		self.ISBN = ""  # ISBN
		self.baozhuang = ""  # 包装

	def trade(self, word):
		if "作者：" and word != "作者：" in word:
			self.zuozhe = word
		if "书号：" and word != "书号：" in word:
			self.shuhao = word
		if "定价：" and word != "定价：" in word:
			self.dingjia = word
		if "字数：" and word != "字数：" in word:
			self.zishu = word
		if "印次：" and word != "印次：" in word:
			self.yinci = word
		if "开本：" and word != "开本：" in word:
			self.kaiben = word
		if "出版时间：" and word != "出版时间：" in word:
			self.chubanshijian = word
		if "ISBN：" and word != "ISBN：" in word:
			self.ISBN = word
		if "包装：" and word != "包装：" in word:
			self.baozhuang = word

	def get_basic_str(self):
		bar = [self.zuozhe, self.shuhao, self.dingjia, self.zishu, self.yinci, self.kaiben, self.chubanshijian,
		       self.ISBN, self.baozhuang]
		return bar

	def trade_title(self, str1):
		title = re.split('\(', str1)
		title = re.split('（', title[0])
		title = title[0].replace('《', '')
		title = title.replace('》', '')
		return title
