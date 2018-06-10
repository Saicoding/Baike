import datetime as d

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from edit.book_zgrm_edit import Bookzgrm
from edit.edit_funs import EditFuns
from model import myunit
from model.function import bar_pop, pop
from page_object.trade_login import *

# 设置无头还是有头
myunit.StartEnd.headless = False


class EditBaike(myunit.StartEnd):
	def test_edit(self):
		mod = {
			'order': 4,  # 1顺序，2随机，3倒叙,4单点
			'each_num': 10,  # 表示每个帐户编辑的词条数
			'index': 16  # 从第几个账号开始4
		}
		start_user_index = mod['index']
		users = [
			{'name': '欢乐麻酱', 'password': 'ty11202'},  # ————————————————1
			{'name': 'sukyyear', 'password': 'ty11202'},  # ———————————————2
			{'name': '天使焦7000', 'password': 'ty11202'},  # ——————————————3
			{'name': '神刀门们主', 'password': 'ty11202'},  # ——————————————4
			{'name': '让子弹跑路', 'password': 'ty11202'},  # ——————————————5
			{'name': '干扰者狂魔', 'password': 'ty11202'},  # ——————————————6
			{'name': '寒帝神牛', 'password': 'ty11202'},  # ————————————————7
			{'name': 'DOTA军团指挥官', 'password': 'ty11202'},  # ———-----——8
			{'name': '福瑞斯听我说', 'password': 'ty11202'},  # ————————————9
			{'name': '威海uncle', 'password': 'ty11202'},  # ——————————————10
			{'name': '这这亮响', 'password': '7788ty'},  # ————————————————11
			{'name': '真没意思的', 'password': 'ya5326249'},  # ————————————12
			{'name': '看似不懂算了', 'password': '2011taosiyuan'},  # ——————13
			{'name': '亮仔美睸', 'password': 'ty11202'},  # ———————————————14
			{'name': '超凡入胜007', 'password': 'ty11202'},  # —————————————15
			{'name': 'saicodings', 'password': 'ty11202'},  # —————————————16
			{'name': '永恒领凡', 'password': 'qwer123'},  # ————————————————17
			{'name': '杭州同济医院v', 'password': 'ty11202'},  # ———————————18
			{'name': '何风一来风', 'password': 'rrt332'},  # ———————————————19
		]
		# 开始时间
		start_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		# 实例化对象
		edit_funs = EditFuns()
		last_user_name = ''
		user_info = ''
		book_zgrm = Bookzgrm(self.driver)
		num1 = {'num': 1}

		while True:
			# arg1:表示模式1顺序，2随机，3倒叙，4单个，arg2：表示每个帐户创建的词条数，arg3:表示从第几个账号开始，
			user = edit_funs.mod(users, mod, start_user_index)

			# 单个词条创建结束
			if user == 4:
				edit_funs.end_sigal_user_edit(start_time, edit_funs, users, mod)
				break
			# 顺序或者倒序结束
			if user == 1 or user == 2:
				edit_funs.end_order_user_edit(start_time, edit_funs, user_info)
				break

			if last_user_name != user['name']:
				last_user_name = user['name']
				# 设置定位器，登陆账号等信息
				options = {
					'username': user['name'],
					'password': user['password'],
					'base_url': 'https://passport.baidu.com/v2/?login',
					'username_loc': (By.ID, "TANGRAM__PSP_3__userName"),
					'password_loc': (By.ID, "TANGRAM__PSP_3__password"),
					'submit_loc': (By.ID, "TANGRAM__PSP_3__submit"),
					'pass_loc': (By.ID, "displayUsername"),
					'fail_loc': (By.ID, "TANGRAM__PSP_3__error"),
					'trade_loc': (By.ID, "TANGRAM__PSP_3__footerULoginBtn"),
					'url': ''
				}
				po = LoginBaike(self.driver, options)
				# 开始登陆
				po.login_action()
				# 等待页面加载指定的元素出现
				WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'mod_feedback')))
				self.driver.get('https://baike.baidu.com/usercenter/lemmas#passed')
				WebDriverWait(self.driver, 10, 0.5).until(
					EC.presence_of_element_located((By.CLASS_NAME, 'list-container')))
				# 得到页面用户信息
				info = edit_funs.get_current_user_info(self.driver, user)
				print(info)
				pop(bar_pop, [1, info])
				user_info += info

			# 得到初始编辑url
			get_book_url = edit_funs.get_book_url()

			# 导航到网址，并得到结果
			if len(get_book_url) == 0:
				print('书目录已空')
				pop(bar_pop, [1, '书目录已空'])
				break
			else:
				book_zgrm.go_to_detal_page(get_book_url[0])
				result = book_zgrm.get_result()

			# 下载图片，判断图片是否存在(如果图片不存在下载时会有弹窗)
			self.driver.get(result['down_url'])
			try:
				alert = self.driver.switch_to.alert
				print('没有图片')
				alert.accept()
				result['down_url'] = ''
				pass
			except:
				pass

			self.driver.get('https://baike.baidu.com/item/' + result['title'])

			page_title = self.driver.title

			if (page_title == "百度百科——全球最大中文百科全书" or page_title == "百度百科_全球最大中文百科全书"):
				edit_funs.trade_fail_open_url(get_book_url)
			else:
				# 判断修改次数
				url = 'https://baike.baidu.com/item/' + result['title']
				times = edit_funs.justfy_edit_times(self.driver, url)
				if times == '1':

					# 编辑词条
					WebDriverWait(self.driver, 10, 0.5).until(
						EC.presence_of_element_located((By.CLASS_NAME, 'lemmaWgt-promotion-rightPreciseAd')))
					num = self.driver.find_element_by_css_selector('.lemmaWgt-promotion-rightPreciseAd').get_attribute(
						"data-lemmaid")
					# 打开词条连接
					self.driver.get('http://baike.baidu.com/edit/1/' + str(num))
					is_new = False
					try:
						WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, 'introjs-skipbutton')))
						is_new = True
					except:
						pass
					finally:
						if is_new:
							print( '是真的' )
							self.driver.find_element_by_id('introjs-skipbutton').click()
					WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'bke_title')))
					# 添加基本信息栏
					edit_funs.add_card(self.driver, result)
					sleep(2)

					# 添加概述图
					edit_funs.add_summary_pic(self.driver, result)
					sleep(5)

					# 切换到编辑界面
					self.driver.switch_to_frame('ueditor_0')

					# 编辑正文
					edit_funs.add_content(self.driver, result)

					sleep(10)
					# 编辑成功后的处理
					edit_funs.treatment_success_edit(get_book_url)
					# 发送消息
					edit_funs.send_message(result, num1)
				else:
					edit_funs.trade_fail_open_url(get_book_url)
					dd
