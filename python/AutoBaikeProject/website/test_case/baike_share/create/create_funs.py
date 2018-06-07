# -*- coding: utf-8 -*-
# @Time :2018/05/30 下午4:21
# @Author : Sanyan
# @File : form_data
# ***************************************
# ****                               ****
# ****  该文档是处理创建百科所需要的方法
# ****                               ****
# ***************************************


import json,random
import os,requests,time
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib import parse
import datetime as d
from model import function
from model.function import bar_pop,pop

class CreateFuns():
	# 在哪里调用这个方法，就返回该方法文件所在的目录
	func_path = os.path.dirname(__file__)
	# 获得上一级目录
	base_dir = os.path.dirname(func_path)
	# 把路径换成字符串，并把‘\’转为‘/’
	base_dir = str(base_dir)
	base_dir = base_dir.replace('\\', '/')
	# 把路径以‘/website'为分割点分离
	base = base_dir.split('/website')[0]
	ini_path = base + '/website/test_data/create.ini'
	all_created_baike_path = base + '/website/test_data/all_created_baike.txt'

	# 打开ini文件并以json格式输出
	def open_ini_result_object(self):
		# 打开ini文件
		ini = open(self.ini_path, 'r', encoding='utf-8')
		ini_content = ini.read()
		ini.close()
		result = json.loads(ini_content)
		return result

	# 打开all_created_baike.txt
	def save_all_created_baike(self,result):
		all_baike = open(self.all_created_baike_path, 'a', encoding='utf-8')
		if len(result['directory']) > 20:
			all_baike.write(result['url']+'\n')
		all_baike.close()
	# 保存
	def save_ini(self, result):
		res_str = json.dumps(result)
		ini_write = open(self.ini_path, 'w', encoding='utf-8')
		ini_write.write(res_str)
		ini_write.close()

	# 创建百科存在和不存在时的处理方法
	def treatment_not_exist_baike(self, create_funs,start_id):
		# 如果创建的词条名称存在，那么book_index 加1
		result = create_funs.open_ini_result_object()
		result['book_index'] += 1
		if result['book_index'] > 10:
			result['book_index'] = 1
			result['book_zgrm_start_id'] += 1
			start_id += 1
		# 保存变化
		create_funs.save_ini(result)

	# 创建百科成功后的处理方法
	def treatment_success_create(self,create_funs,start_id):
		# 如果创建成功，那么book_index 加1
		result = create_funs.open_ini_result_object()
		result['current_create_index'] += 1
		result['book_index'] += 1
		if result['book_index'] > 10:
			result['book_index'] = 1
			result['book_zgrm_start_id'] += 1
			start_id += 1
		# 保存变化
		create_funs.save_ini(result)


	def get_baike(self,result):
		baike = {}
		baike['title'] = result['title']
		baike['boundary'] = '----WebKitFormBoundary' + str(random.randint(1e16, 1e17 - 1))
		baike['author'] = result['author']
		baike['referance'] =result['url']
		baike['date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		baike['lemmaTime'] = str(random.randint(100,500))
		baike['message'] ='<h2>基本信息</h2><p>作者：'+result['author']+'</p><p>'+result['bar'][1]+'</p><p>'+result['bar'][2]+'</p><p>'+result['bar'][3]+'</p><p>'+result['bar'][4]+'</p><p>'+result['bar'][5]+'</p><p>'+result['bar'][6]+'</p><p>'+result['bar'][7]+'</p><p>'+result['bar'][8]+'</p><h2>内容简介</h2><p>&nbsp;&nbsp;'+result['content']+'<sup data-type="reference" unselectable="on" class="ref" src="http://baike.bdimg.com/img/baike/editor/reference.gif" data-id="1"></sup></p><p><br/>　　</p><p><br/></p>'
		return baike
	# 发送各种消息
	def send_message(self,result,num):
		directory = result['directory']

		info = ''
		if len(directory) > 20:
			info = ',有目录'
		info = '当前第'+str(num['num'])+'个词条,标题是:'+result['title']+info
		print(info)
		pop(bar_pop,[0,info])
		num['num'] += 1


	def create(self,baike,cookiestr):
		url = "http://baike.baidu.com/submitcreate"
		title = parse.quote(baike['title'])
		ref = 'http://baike.baidu.com/create/' + title
		content_type = 'multipart/form-data; boundary='+baike['boundary']
		headers = {
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'Origin': 'http://baike.baidu.com',
			'Upgrade-Insecure-Requests': '1',
			'Content-Type': content_type,
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Referer': ref,
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Cookie': cookiestr
		}
		multipart_encoder = MultipartEncoder(
			fields={
				'preFlag': '',
				'album': '',
				'video': '',
				'map': '',
				'abstract': '{"imgSrc":"","imgTitle":"","summaryContent":"<p>《' + baike['title'] + '》是2018年中国人民大学出版社出版书籍，作者是' + baike['author'] + '。</p>","width":"","height":"","picId":"","owner":""}',
				'moduleContent': '{}',
				'reference': '[{"type":1,"title":"' + baike['title'] + '","url":"' + baike['referance'] + '","site":"中国人民大学出版社","publishDate":"","refDate":"' + baike['date'] + '","index":1}]',
				'card': '{"type":"","content":[]}',
				'classify': '',
				'draftId': '0',
				'draftType': '',
				'extAlbumData': '',
				'personal': 'null',
				'series': '',
				'tuwen': '',
				'music': '',
				'commonModuleList': '',
				'callback': 'POST_CREATE_CALLBACK',
				'lemmaTime': baike['lemmaTime'],
				'lemmaVersionId': '',
				'beforeLemma': '',
				'endLemma': '',
				'paragraphNum': '',
				'lemmaTitle': baike['title'],
				'lemmaid': '',
				'extDataInit': '',
				'summaryImgIdInit': '',
				'summaryImgInfoInit': '',
				'summarySummaryInit': '',
				'extDataTypeInit': '',
				'extDataTypeTempInit': '',
				'isCreate': '1',
				'isSectionEdit': '0',
				'message': baike['message'],
				'lemmamodify': '创建义项',
				'oriDesc': '',
				'subLemmaDesc': '',
				'createlemma': ' 提 交 ',
				'propsId': '',
				'propsClassId': '',
				'mc_al_name': '请输入专辑名称',
				'mc_al_date': '2011-03-04',
				'mc_al_lge': '国语',
				'mc_al_type': 'other',
				'mc_al_com': '',
				'mc_al_rec': '',
				'mc_al_userd_key_0': '',
				'mc_al_song_0': '',
				'title': '第1集',
				# 'editorValue': baike['editorValue']
			},
			boundary = baike['boundary']
		)

		r = requests.post(url, data=multipart_encoder, headers=headers)
		return r

	# 处理时间
	def str_to_int(self, str1):
		int1 = 0
		if len(str1) == 16:
			int1 = int(str1[0:4]+str1[5:7]+str1[8:10]+str1[11:13]+str1[14:16])
		elif len(str1) == 19:
			int1 = int(str1[0:4]+str1[5:7]+str1[8:10]+str1[11:13]+str1[14:16]+str1[17:19])
		return int1

	# 创建百科选择账号得模式
	def mod(self,users,mod,start_user_index ):
		result = self.open_ini_result_object()
		current_index= result['current_create_index']
		len1 = len(users)
		if current_index >= mod['each_num']:
			if mod['order'] == 1: # 顺序
				# 先判断是否结束
				if mod['index'] == start_user_index-1: # 到一圈了，要结束
					result['current_create_index'] = 0
					self.save_ini(result)
					return 1
				else:
					if mod['index'] == len1:
						mod['index'] = 1
					else:
						mod['index'] += 1
					user = users[mod['index'] - 1]
					result['current_create_index'] = 0
					self.save_ini(result)
					return user

			elif mod['order'] ==2: # 倒序
				if mod['index'] == start_user_index+1: # 到一圈了，要结束
					return 2
				else:
					if mod['index'] == 1:
						mod['index'] = len1
					else:
						mod['index'] -= 1
					user = users[mod['index'] - 1]
					result['current_create_index'] = 0
					self.save_ini(result)
					return user
			elif mod['order'] == 3: # 随机
				mod['index'] = random.randint(0, 20)
				user = users[mod['index'] - 1]
				result['current_create_index'] = 0
				self.save_ini(result)
				return user

			elif mod['order'] == 4: # 单个账号
				result['current_create_index'] = 0
				self.save_ini(result)
				return 4

		self.save_ini(result)
		user = users[mod['index'] - 1]
		return user

	# 单个账号创建百科结束
	def end_sigal_user_create(self,start_time,create_funs,users,mod):
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 结束时间
		start = create_funs.str_to_int(start_time)
		end = create_funs.str_to_int(end_time)
		num = (end - start) / 60
		m = int(num)
		s = (end - start) - m * 60
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		index = mod['index']-1
		user = users[index]
		info = '账号：' + user['name'] + '已创建' + str(mod['each_num']) + '个词条（结束）,开始时间:' + start_time + ',结束时间:' + end_time + ',用时' + str(m) + '分' + str(s) + '秒'
		function.send_statics_email(info)
		print(info)
		pop(bar_pop, [0, info])

	# 顺序或者倒序结束
	def end_order_user_create(self,start_time, create_funs,user_info):
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 结束时间
		start = create_funs.str_to_int(start_time)
		end = create_funs.str_to_int(end_time)
		num = (end - start) / 60
		m = int(num)
		s = (end - start) - m * 60
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		info = user_info+'顺序循环结束,开始时间:' + start_time + ',结束时间:' + end_time + ',用时' + str(m) + '分' + str(s) + '秒'
		function.send_statics_email(info)
		pop(bar_pop, [0, info])

	# 得到账号信息
	def get_current_user_info(self,driver,user):
		# 等级
		leavel = driver.find_element_by_css_selector('body > div.main-header > div.base-info > div > div.user-info.cmn-inline-block > div.level-mark > i.curr-level').text
		# 通过率
		pass_rate= driver.find_element_by_css_selector('body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li:nth-child(6) > i').text
		#提交版本
		submit_num = driver.find_element_by_css_selector('body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li.simple.margin-left > i').text
		# 通过版本
		succeed_num = driver.find_element_by_css_selector('body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li:nth-child(1) > a > dl > dd').text
		# 创建版本
		create_num = driver.find_element_by_css_selector('body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li:nth-child(8) > i').text
		# 财富值
		score = driver.find_element_by_css_selector('body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > div > div > label > i').text

		str = '账号：'+user['name']+',等级：'+leavel+',通过率：'+pass_rate+',提交版本：'+submit_num+'个,通过版本'+succeed_num+'个,创建版本'+create_num+'个，财富值:'+score+'\n'
		return str











