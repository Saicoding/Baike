from model import myunit
from baike_share.monitor.monitor_funs import MonitorFuns

# 设置无头还是有头
myunit.StartEnd.headless = True


class Monitor(myunit.StartEnd):
	def test_monitor(self):
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
			{'name': '百科代王', 'password': '5678ey'},  # ——————————————20
		]

		# 实例化对象
		monitor_funs = MonitorFuns(self.driver)

		while True:
			# 打开要统计信息的url和user
			url = monitor_funs.get_url(users)['url']
			user = monitor_funs.get_url(users)['user']
			self.driver.get(url)

			# 得到页面所有的信息的状态
			status_list = monitor_funs.get_status(users)
			if status_list == False:
				continue
			# 处理信息的变化
			monitor_funs.trade_modify(status_list, user['name'], users)
