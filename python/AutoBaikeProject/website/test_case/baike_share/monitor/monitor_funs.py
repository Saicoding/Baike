import os, json
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from model.function import bar_pop, pop


class MonitorFuns():
	def __init__(self, driver):
		self.driver = driver

	# 在哪里调用这个方法，就返回该方法文件所在的目录
	func_path = os.path.dirname(__file__)
	# 获得上一级目录
	base_dir = os.path.dirname(func_path)
	# 把路径换成字符串，并把‘\’转为‘/’
	base_dir = str(base_dir)
	base_dir = base_dir.replace('\\', '/')
	# 把路径以‘/website'为分割点分离
	base = base_dir.split('/website')[0]
	ini_path = base + '/website/test_data/monitor.ini'

	# 打开ini文件并以json格式输出
	def open_ini_result_object(self):

		# 打开ini文件
		ini = open(self.ini_path, 'r', encoding='utf-8')
		ini_content = ini.read()
		ini.close()
		result = json.loads(ini_content)
		return result

	# 保存
	def save_ini(self, result):
		res_str = json.dumps(result)
		ini_write = open(self.ini_path, 'w', encoding='utf-8')
		ini_write.write(res_str)
		ini_write.close()

	# 得到需要查询状态的url
	def get_url(self, users):
		result = self.open_ini_result_object()
		index = result['current_index']
		user = users[index]
		url = 'https://www.baidu.com/p/' + user['name'] + '?from=wk'
		return {'user': user, 'url': url}

	# 得到页面所有的信息的状态
	def get_status(self,users):
		is_true = True
		list1 = []
		try:
			WebDriverWait(self.driver, 10, 0.5).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, '.product-page')))
			iframe = self.driver.find_element_by_css_selector('.product-page')
			self.driver.switch_to_frame(iframe)
			sleep(1)
			level = self.driver.find_element_by_css_selector(
				'.block-level > div:nth-child(1) > h3:nth-child(1) > b:nth-child(1)').text  # 等级
			score = self.driver.find_element_by_css_selector(
				'.block-level > div:nth-child(1) > h3:nth-child(1) > b:nth-child(2)').text  # 经验值
			money = self.driver.find_element_by_css_selector(
				'.block-level > div:nth-child(1) > h3:nth-child(2) > b:nth-child(1)').text  # 财富值
			pass_num = self.driver.find_element_by_css_selector(
				'.version_content_pie > div:nth-child(3) > span:nth-child(1)').text  # 通过版本数
			rate = self.driver.find_element_by_css_selector(
				'.ratio_content_pie > div:nth-child(3) > span:nth-child(1)').text  # 通过率
			latest_modify_time = self.driver.find_element_by_css_selector(
				'.list-container > tr:nth-child(1) > td:nth-child(3)').text  # 最近通过时间
			list1 = [level, score, money, pass_num, rate, latest_modify_time]
		except:
			is_true = False
		finally:
			if is_true == False:
				result = self.open_ini_result_object()
				result['current_index'] += 1
				if result['current_index'] == len(users):
					result['current_index'] = 0
				self.save_ini(result)
				print('元素没找到，过一个')
				pop(bar_pop, [3, '元素没找到，过一个'])
				return False
			else:
				return list1

	# 处理信息的变化
	def trade_modify(self, status_list, user, users):
		result = self.open_ini_result_object()
		index = result['current_index']
		info = user + '=>'
		sleep(5)
		# 开始启动,就初始化值
		if result['start_status'] == [] or len(result['start_status']) < len(users):
			result['start_status'].append(status_list)
		# 没有变化
		elif result['start_status'][index] == status_list:
			pass
		# 有了变化
		elif result['start_status'][index] != status_list:
			# a ={'w':result['start_status'][index],'index':index}
			# b = {'w':status_list,'index':index}
			# print(json.dumps(a)+'')
			# print(json.dumps(b))

			origin_list = result['start_status'][index]
			if status_list[3] != origin_list[3]:  # 通过版本数
				sub = int(status_list[3]) - int(origin_list[3])
				result['start_status'][index][3] = status_list[3]
				info += "通过了" + str(sub) + "个版本,"
				pop(bar_pop, [3, info])

			if status_list[0] != origin_list[0]:  # 等级
				result['start_status'][index][0] = status_list[0]
				info += "升级啦!从" + origin_list[0] + "升到" + status_list[0] + ","
				pop(bar_pop, [3, info])

			if status_list[1] != origin_list[1]:  # 经验值
				sub = int(status_list[1]) - int(origin_list[1])
				result['start_status'][index][1] = status_list[1]
				info += "总分经验值" + status_list[1] + "增加了" + str(sub) + ","
				pop(bar_pop, [3, info])

			if status_list[2] != origin_list[2]:  # 财富值
				info += "当前财富值" + status_list[2] + ","
				result['start_status'][index][2] = status_list[2]
				pop(bar_pop, [3, info])

			if status_list[4] != origin_list[4]:  # 通过率
				sub = int(status_list[4]) - int(origin_list[4])
				result['start_status'][index][4] = status_list[4]
				if sub > 0:
					info += "通过率提升" + str(sub) + "%,"
					pop(bar_pop, [3, info])
				if sub < 0:
					info += "通过率降低" + str(sub) + "%,"
					pop(bar_pop, [3, info])

			info += '通过率' + result['start_status'][index][4] + '%,'
			if status_list[5] != origin_list[5]:  # 最后通过时间
				result['start_status'][index][5] = status_list[5]
				info += "最后通过时间" + status_list[5]
				pop(bar_pop, [3, info])
				print(info)

		result['current_index'] += 1

		if result['current_index'] == len(users):
			result['current_index'] = 0

		# 保存变化
		self.save_ini(result)
