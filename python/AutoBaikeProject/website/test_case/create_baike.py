from selenium.webdriver.common.by import By
from model import myunit
from page_object.trade_login import *
import unittest
from create.create_funs import CreateFuns
from create.book_zgrm_create import Bookzgrm
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as d
from model.function import bar_pop, pop

# 设置无头还是有头
myunit.StartEnd.headless = True


class CreateBaike(myunit.StartEnd):
	def test_login(self):
		mod = {
			'order': 4,  # 1顺序，2随机，3倒叙,4单点
			'each_num': 10,  # 表示每个帐户创建的词条数
			'index': 3  # 从第几个账号开始
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
			{'name': '百科代王', 'password': '5678ey'},  # —————————————————20
		]

		# 开始时间
		start_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		# 实例化对象
		book_zgrm = Bookzgrm(self.driver)
		create_funs = CreateFuns()
		user_info = ''
		last_user_name = ''
		cookiestr = ''
		num = {'num': 1}
		while True:
			# arg1:表示模式1顺序，2随机，3倒叙，4单个，arg2：表示每个帐户创建的词条数，arg3:表示从第几个账号开始，
			user = create_funs.mod(users, mod, start_user_index)

			# 单个词条创建结束
			if user == 4:
				create_funs.end_sigal_user_create(start_time, create_funs, users, mod)
				break
			# 顺序或者倒序结束
			if user == 1 or user == 2:
				create_funs.end_order_user_create(start_time, create_funs, user_info)
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
				info = create_funs.get_current_user_info(self.driver, user)
				print(info)
				# 弹出系统气泡
				pop(bar_pop, [0, info])
				user_info += info
				# 得到cookie
				cookie = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
				cookiestr = ';'.join(item for item in cookie)

			# 得到初始搜索ID
			start_id = book_zgrm.get_start_page_num(create_funs)

			# 导航到这个初始ID的页面
			book_zgrm.go_to_start_page(start_id)

			# 等待5秒，让保证页面载入完全,然后找到要点击的链接
			book_zgrm.go_detail_page(create_funs)

			# 得到百科创建的标题和基本信息栏，内容，作者等
			result = book_zgrm.get_result()

			# 判断如果内容为空，就继续下个循环
			if result['content'] == "":
				create_funs.treatment_not_exist_baike(create_funs, start_id)
				continue
			# 打开创建页面
			self.driver.get('http://baike.baidu.com/create/' + result['title'])

			# 判断创建的词条名称是否存在
			if self.driver.title == "百度百科——全球最大中文百科全书" or self.driver.title == "百度百科_全球最大中文百科全书":
				create_funs.treatment_not_exist_baike(create_funs, start_id)
			# 词条名称不存在就开始创建
			else:
				# 创建词条
				baike = create_funs.get_baike(result)
				create_funs.create(baike, cookiestr)
				# 保存创建的词条
				create_funs.save_all_created_baike(result)
				# 创建成功后的处理
				create_funs.treatment_success_create(create_funs, start_id)
				# 发送消息
				create_funs.send_message(result, num)

if __name__ == '__main__':
	unittest.main()
