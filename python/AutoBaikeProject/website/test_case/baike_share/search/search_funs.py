import os
import json
import re
import time
import pytz
from model.function import bar_pop,pop,send_statics_email


class SearchFuns():
	# 在哪里调用这个方法，就返回该方法文件所在的目录
	func_path = os.path.dirname(__file__)

	# 获得上一级目录
	base_dir = os.path.dirname(func_path)

	# 把路径换成字符串，并把‘\’转为‘/’
	base_dir = str(base_dir)
	base_dir = base_dir.replace('\\', '/')

	# 把路径以‘/website'为分割点分离
	base = base_dir.split('/website')[0]
	file_ini = base+'/website/test_data/search.ini'

	# 需要写入的文件路径
	file_max_num_path = "F:\\Saicode\\api\\baike\\baike\\max_num.json"
	file_max_id_path = "F:\Saicode\\api\\baike\\baike\max_id.json"
	file_time_path = "F:\Saicode\\api\\baike\\baike\\time.json"

	# 得到ini对应key的值
	def get_ini(self, key):
		with open(self.file_ini, 'r') as file:
			ini = file.read()
			result = json.loads(ini)
			result_key = str(result[key])
			return result_key

	def open_ini_result_object(self):
		# 打开ini文件
		file_ini = open(self.file_ini, 'r', encoding='utf-8')
		file_content = file_ini.read()
		file_ini.close()
		result = json.loads(file_content)
		return result

	def write_str_result_to_ini(self, result):
		res_str = json.dumps(result)
		file_ini_write = open(self.file_ini, 'w', encoding='utf-8')
		file_ini_write.write(res_str)
		file_ini_write.close()

	def get_start_time(self):
		result = self.open_ini_result_object()
		start_time = result['latest_c_time']
		start_time = self.str_to_int(start_time)
		return start_time

	def open_page_num_file(self, pageNum, r_w):
		filePath = "F:\\Saicode\\api\\baike\\all\\"+pageNum+".json"

		page_num_file = open(filePath, r_w, encoding='utf-8')
		return page_num_file

	# 将得到的内容整理成方便写入pageNumFile的数组
	# 2018-05-17 20:12 查看 神刀门们主 比速T5分手动档和自动档，上市时间不一样，更明。
	# 2018-06-18 20:13 查看 主任 修改目录。
	def get_list_str(self, content, title, num):
		modify_time = ""
		modify_user = ""
		modify_reson = ""
		create_time = ""
		create_user = ""
		create_reson = ""
		id = self.get_ini("id")
		now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))

		# 以换行符为分割点
		content = content.replace("\s+本人\s+)", " ")
		content = re.sub("\s+本人\s+"," ", content)
		con_array = re.split(r'\n', content)

		times = str(len(con_array))
		i = 0
		for con in con_array:
			singal_line_array = con.strip()
			singal_line_array = re.split(r'\s', singal_line_array)
			if i == 0:
				modify_time = singal_line_array[0] +" "+singal_line_array[1]
				modify_user = singal_line_array[3]
				modify_reson = singal_line_array[4]

			if i == len(con_array)-1:
				create_time = singal_line_array[0] +" "+singal_line_array[1]
				create_user = singal_line_array[3]
				j = 0
				for singal_line in singal_line_array:
					if j >= 4:
						modify_reson += singal_line+" "
					create_reson = singal_line_array[4]

			i = i + 1

		res = [id, title, num, create_time, create_user, create_reson, modify_time, modify_user, modify_reson, now, times]

		return res

	def write_to_page_num(self, list_str, page_num):
		page_num_file_r = self.open_page_num_file(page_num, "r")  # 打开page_num_file
		page_num_file_r.seek(0, 0)
		content = page_num_file_r.read()  # 读取所有行
		page_num_file_r.close()
		content = content[:-2]  #删除最后两个字符

		all = int(self.get_ini('all'))
		page_num_file_w = self.open_page_num_file(page_num, "w")

		if all > 0:
			page_num_file_w.write(content + ',\n{"id":'+list_str[0]+',"title":"'+list_str[1]+'","num":'+list_str[2]+',"create_time":"'+list_str[3]+'","creat_user":"'+list_str[4]+'","creat_reson":"'+list_str[5]+'","modify_time":"'+list_str[6]+'","modify_user":"'+list_str[7]+'","modify_reson":"'+list_str[8]+'","now":"'+list_str[9]+'","times":'+list_str[10]+'}]}')
		if all == 0:
			page_num_file_w.write(content + '\n{"id":' + list_str[0] + ',"title":"' +list_str[1] + '","num":' + list_str[2] + ',"create_time":"' + list_str[3] + '","creat_user":"' + list_str[4] + '","creat_reson":"' + list_str[5] + '","modify_time":"' + list_str[6] + '","modify_user":"' + list_str[7] + '","modify_reson":"' + list_str[8] + '","now":"' + list_str[9] + '","times":' + list_str[10] + '}]}')

		page_num_file_w.close()
		all += 1

		if all > 500:
			page_num = str(int(page_num)+1)
			# 创建新的pageNum文件
			filename = "F:\\Saicode\\api\\baike\\all\\"+page_num+".json"
			file = open(filename, 'a', encoding='utf-8')
			file.write('{"data":[]}')
			file.close()

	def str_to_int(self, str1):
		if len(str1) == 16:
			int1 = int(str1[0:4]+str1[5:7]+str1[8:10]+str1[11:13]+str1[14:16])
		elif len(str1) == 19:
			int1 = int(str1[0:4]+str1[5:7]+str1[8:10]+str1[11:13]+str1[14:16]+str1[17:19])
		return int1

	def save_data(self, start_statistics_num,start_statistics_time,res):
		# 打开ini文件
		result = self.open_ini_result_object()

		result['id'] += 1
		result['num'] += 1
		result['all'] += 1
		result['count'] += 1
		if result['all'] > 500:
			result['pageNum'] += 1
			result['all'] = 0

		if result['id'] >= result['maxId']:
			result['maxId'] = result['id']
			maxId = str(result['maxId'])
			with open(self.file_max_id_path, 'w', encoding='utf-8') as file:
				file.write('{"data":[{"maxId":'+maxId+'}]}')

		if  result['num'] > result['maxNum']:
			result['maxNum'] = result['num']
			maxNum = str(result['maxNum'])
			with open(self.file_max_num_path, 'w', encoding='utf-8') as file:
				file.write('{"data":[{"maxNum":'+maxNum+'}]}')

		if self.str_to_int(res[3]) > self.str_to_int(result['latest_c_time']):
			result['latest_c_time'] = res[3]

		if self.str_to_int(res[3]) < self.str_to_int(result['oldest_c_time']):
			result['oldest_c_time'] = res[3]

		if self.str_to_int(res[6]) > self.str_to_int(result['latest_m_time']):
			result['latest_m_time'] = res[6]

		if self.str_to_int(res[6]) < self.str_to_int(result['oldest_m_time']):
			result['oldest_m_time'] = res[6]

		if self.str_to_int(res[9]) > self.str_to_int(result['latest_u_time']):
			result['latest_u_time'] = res[9]

		if self.str_to_int(res[9]) < self.str_to_int(result['oldest_u_time']):
			result['oldest_u_time'] = res[9]

		# 保存各种时间
		with open('F:\\Saicode\\api\\baike\\baike\\time.json', 'w') as f:
			f.write('{"data":[{"latest_c_time":"'+result['latest_c_time'] +'"},{"oldest_c_time":"'+result['oldest_c_time'] +'"},{"latest_m_time":"'+result['latest_m_time'] +'"},{"oldest_m_time":"'+result['oldest_m_time'] +'"},{"latest_u_time":"'+result['latest_u_time'] +'"},{"oldest_u_time":"'+result['oldest_u_time'] +'"}]}')

		# 保存更改的ini文件
		self.write_str_result_to_ini(result)

	def save_num(self):
		# 打开ini文件
		result = self.open_ini_result_object()
		result['num'] += 1

		self.write_str_result_to_ini(result)

	def decide_to_break(self, mode, num, start_time):
		if mode == 'count':
			result = self.open_ini_result_object()
			count = result['count']
			if count > num:
				result['count'] = 0
				self.write_str_result_to_ini(result)
				return True

		if mode == 'time':
			result = self.open_ini_result_object()
			last_time = self.str_to_int(result['latest_c_time'])
			if last_time - start_time > num:
				result['start_time'] = ""
				self.write_str_result_to_ini(result)
				return True

	def get_start_info(self):
		result =self.open_ini_result_object()
		return result

	def get_end_info(self):
		result = self.open_ini_result_object()
		return result

	# 统计各种数据
	def statistics(self,start_statistics_num,start_statistics_time,list_str):
		# 获取当前时间
		tz = pytz.timezone('Asia/Shanghai')
		# current_time = str(datetime.datetime.now(tz))[0:16]

		# 获取当前的create_time的数字
		current_create_time = list_str[3][11:16]
		current_create_time = int(current_create_time[0:2]+current_create_time[3:6])
		current_create_time = current_create_time

		# 打开ini文件
		result = self.open_ini_result_object()
		# 如果没有检查过
		if result['is_check'] == 0:
			# 当当前创建时间超过早上9点的时候记录当前、当前前一天、当前前一天的一天的id
			if ((current_create_time >= 915) and (current_create_time <= 1000) ):
				result['is_check'] = 1
				num1 = str(int(list_str[0]) - int(result["today_id"]))
				num1_perhour = str(round((int(list_str[0]) - int(result["today_id"]))/24,1))
				result['pre_pre_day_id'] = result['pre_day_id']
				result['pre_day_id'] = result["today_id"]
				result['today_id'] = list_str[0]

				info = "过去一天有"+num1+"个词条,平均一小时"+num1_perhour+"个"
				pop(bar_pop, [2, '更新统计：'+info])
				send_statics_email(info)
		self.write_str_result_to_ini(result)
		if current_create_time > 1000:
			result['is_check'] = 0
			self.write_str_result_to_ini(result)
		# 得到早上到目前的创建词条数
		today_num = str(int(list_str[0]) - int(result["today_id"]))

		# 得到早上到现在平均每小时多少个词
		sub_minute = (current_create_time - 915)/60
		if sub_minute == 0:		# 防止sub_minute=0
			sub_minute =1
		today_persent = str(round(int(today_num)/sub_minute,1))

		# 前一天总数
		pre_num = str(int(result["today_id"]) - int(result['pre_day_id']))
		# 前一天平均
		pre_persent = str(round(int(pre_num)/24,1))
		# 大前天总数
		pre_pre_num = str(int(result['pre_day_id']) - int(result['pre_pre_day_id']))
		# 大前天平均
		pre_pre_persent = str(round(int(pre_pre_num) / 24, 1))
		if int(result['count']) % 100 ==0:
			info = "最后创建时间"+list_str[3]+",早上到目前："+today_num+"个,平均一小时:"+today_persent+"个,前一天总数:"+pre_num+"个,前一天平均一小时"+pre_persent+"个，大前天总数"+pre_pre_num+"个，大前天平均一小时"+pre_pre_persent+"个,当前词："+list_str[1]+",当前num:"+list_str[2]
			print(info)
			pop(bar_pop,['2',info])
