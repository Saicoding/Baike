import json, random
import os, time
import datetime as d
from model import function
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from model.function import bar_pop, pop


class EditFuns():
	# 在哪里调用这个方法，就返回该方法文件所在的目录
	func_path = os.path.dirname(__file__)
	# 获得上一级目录
	base_dir = os.path.dirname(func_path)
	# 把路径换成字符串，并把‘\’转为‘/’
	base_dir = str(base_dir)
	base_dir = base_dir.replace('\\', '/')
	# 把路径以‘/website'为分割点分离
	base = base_dir.split('/website')[0]
	ini_path = base + '/website/test_data/edit.ini'
	all_created_baike_path = base + '/website/test_data/all_created_baike.txt'

	# 打开ini文件并以json格式输出
	def open_ini_result_object(self):
		# 打开ini文件
		ini = open(self.ini_path, 'r', encoding='utf-8')
		ini_content = ini.read()
		ini.close()
		result = json.loads(ini_content)
		return result

	# 处理时间
	def str_to_int(self, str1):
		int1 = 0
		if len(str1) == 16:
			int1 = int(str1[0:4] + str1[5:7] + str1[8:10] + str1[11:13] + str1[14:16])
		elif len(str1) == 19:
			int1 = int(str1[0:4] + str1[5:7] + str1[8:10] + str1[11:13] + str1[14:16] + str1[17:19])
		return int1

	# 保存
	def save_ini(self, result):
		res_str = json.dumps(result)
		ini_write = open(self.ini_path, 'w', encoding='utf-8')
		ini_write.write(res_str)
		ini_write.close()

	def mod(self, users, mod, start_user_index):
		result = self.open_ini_result_object()
		current_index = result['current_edit_index']
		len1 = len(users)
		if current_index >= mod['each_num']:
			if mod['order'] == 1:  # 顺序
				# 先判断是否结束
				if mod['index'] == start_user_index - 1:  # 到一圈了，要结束
					result['current_edit_index'] = 0
					self.save_ini(result)
					return 1
				else:
					if mod['index'] == len1:
						mod['index'] = 1
					else:
						mod['index'] += 1
					user = users[mod['index'] - 1]
					result['current_edit_index'] = 0
					self.save_ini(result)
					return user

			elif mod['order'] == 2:  # 倒序
				if mod['index'] == start_user_index + 1:  # 到一圈了，要结束
					return 2
				else:
					if mod['index'] == 1:
						mod['index'] = len1
					else:
						mod['index'] -= 1
					user = users[mod['index'] - 1]
					result['current_edit_index'] = 0
					self.save_ini(result)
					return user
			elif mod['order'] == 3:  # 随机
				mod['index'] = random.randint(0, 20)
				user = users[mod['index'] - 1]
				result['current_edit_index'] = 0
				self.save_ini(result)
				return user

			elif mod['order'] == 4:  # 单个账号
				result['current_edit_index'] = 0
				self.save_ini(result)
				return 4

		self.save_ini(result)
		user = users[mod['index'] - 1]
		return user

	# 单个账号创建百科结束
	def end_sigal_user_edit(self, start_time, edit_funs, users, mod):
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 结束时间
		start = edit_funs.str_to_int(start_time)
		end = edit_funs.str_to_int(end_time)
		num = (end - start) / 60
		m = int(num)
		s = (end - start) - m * 60
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		index = mod['index'] - 1
		user = users[index]
		info = '账号：' + user['name'] + '已编辑' + str(
			mod['each_num']) + '个词条（结束）,开始时间:' + start_time + ',结束时间:' + end_time + ',用时' + str(m) + '分' + str(s) + '秒'
		function.send_statics_email(info)
		print(info)
		pop(bar_pop, [1, info])

	# 顺序或者倒序结束
	def end_order_user_edit(self, start_time, edit_funs, user_info):
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 结束时间
		start = edit_funs.str_to_int(start_time)
		end = edit_funs.str_to_int(end_time)
		num = (end - start) / 60
		m = int(num)
		s = (end - start) - m * 60
		end_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		info = user_info + '顺序编辑循环结束,开始时间:' + start_time + ',结束时间:' + end_time + ',用时' + str(m) + '分' + str(s) + '秒'
		function.send_statics_email(info)
		print(info)
		pop(bar_pop, [1, info])

	# 得到账号信息
	def get_current_user_info(self, driver, user):
		# 等级
		leavel = driver.find_element_by_css_selector(
			'body > div.main-header > div.base-info > div > div.user-info.cmn-inline-block > div.level-mark > i.curr-level').text
		# 通过率
		pass_rate = driver.find_element_by_css_selector(
			'body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li:nth-child(6) > i').text
		# 提交版本
		submit_num = driver.find_element_by_css_selector(
			'body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li.simple.margin-left > i').text
		# 通过版本
		succeed_num = driver.find_element_by_css_selector(
			'body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li:nth-child(1) > a > dl > dd').text
		# 创建版本
		create_num = driver.find_element_by_css_selector(
			'body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > ul > li:nth-child(8) > i').text
		# 财富值
		score = driver.find_element_by_css_selector(
			'body > div.main-header > div.base-info > div > div.baike-info.cmn-inline-block > div > div > label > i').text

		str = '账号：' + user[
			'name'] + ',等级：' + leavel + ',通过率：' + pass_rate + ',提交版本：' + submit_num + '个,通过版本' + succeed_num + '个,创建版本' + create_num + '个，财富值:' + score + '\n'
		return str

	def get_book_url(self):
		f = open(self.all_created_baike_path, 'r', encoding='utf-8')
		lines = f.readlines()

		f.close()
		return lines

	# 判断词条修改次数
	def justfy_edit_times(self, driver, url):
		times = driver.find_element_by_css_selector('dd.description >ul >li:nth-child(2)').text
		# 处理字符串
		times = times.replace('编辑次数：', '')
		times = times.replace('次历史版本', '')
		return times

	def get_baike(self, result):
		baike = {}
		baike['title'] = result['title']
		baike['boundary'] = '----WebKitFormBoundary' + str(random.randint(1e16, 1e17 - 1))
		baike['author'] = result['author']
		baike['referance'] = result['url']
		baike['date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		baike['lemmaTime'] = str(random.randint(100, 500))
		baike['message'] = '<h2>基本信息</h2><p>作者：' + result['author'] + '</p><p>' + result['bar'][1] + '</p><p>' + \
		                   result['bar'][2] + '</p><p>' + result['bar'][3] + '</p><p>' + result['bar'][4] + '</p><p>' + \
		                   result['bar'][5] + '</p><p>' + result['bar'][6] + '</p><p>' + result['bar'][7] + '</p><p>' + \
		                   result['bar'][8] + '</p><h2>内容简介</h2><p>&nbsp;&nbsp;' + result[
			                   'content'] + '<sup data-type="reference" unselectable="on" class="ref" src="http://baike.bdimg.com/img/baike/editor/reference.gif" data-id="1"></sup></p><p><br/>　　</p><p><br/></p><h2>作者介绍</h2><p>' + \
		                   result[
			                   'author_info'] + '&nbsp;<sup data-type="reference" unselectable="on" class="ref" src="http://baike.bdimg.com/img/baike/editor/reference.gif" data-id="1"></sup></p><h2>目录</h2><p>' + \
		                   result[
			                   'directory'] + '<sup data-type="reference" unselectable="on" class="ref" src="http://baike.bdimg.com/img/baike/editor/reference.gif" data-id="1"></sup></p>'
		return baike

	# 如果词条没有创建成功
	def trade_fail_open_url(self, url):
		# 去掉这条url
		url.pop(0)
		f = open(self.all_created_baike_path, 'w', encoding='utf-8')
		f.truncate()
		f.close()
		f1 = open(self.all_created_baike_path, 'a', encoding='utf-8')
		for u in url:
			f1.write(u)
		f1.close()

	def treatment_success_edit(self, url):
		# 去掉这条url
		url.pop(0)
		f = open(self.all_created_baike_path, 'w', encoding='utf-8')
		f.truncate()
		f.close()
		f1 = open(self.all_created_baike_path, 'a', encoding='utf-8')
		for u in url:
			f1.write(u)
		f1.close()
		# 如果创建成功，那么book_index 加1
		result = self.open_ini_result_object()
		result['current_edit_index'] += 1
		# 保存变化
		self.save_ini(result)

	def send_message(self, result, num):
		info = '当前编辑第' + str(num['num']) + '个词条,标题是:' + result['title']
		print(info)
		pop(bar_pop, [1, info])
		num['num'] += 1

	# 添加概述图
	def add_summary_pic(self, driver, result):
		if result['down_url'] == '':
			return
		else:
			driver.find_element_by_id("card-pic-add").click()
			sleep(2)
			iframe = driver.find_element_by_css_selector('.bkdialog-iframe')
			driver.switch_to_frame(iframe)
			# 得到input element
			try:
				driver.find_element_by_css_selector('#filePicker input').send_keys(
					'F:\\WorkPlace\\Python\\python\\AutoBaikeProject\\website\\test_data\\imgs\\' + result[
						'primitive_title'] + '.jpg')
			except:
				driver.find_element_by_css_selector('#filePicker input').send_keys(
					'F:\\WorkPlace\\Python\\python\\AutoBaikeProject\\website\\test_data\\imgs\\' + result[
						'primitive_title'] + '.png')
			driver.switch_to.default_content()
			sleep(2)
			# 点击确定按钮
			driver.find_elements_by_css_selector('.bkdialog-footer > div > div')[0].click()

	# 点击添加基本信息栏
	def add_card(self, driver, result):
		js = "bk.basicInfoBar.insertMainInfo();return false;"
		driver.execute_script(js)
		WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'card-div-1')))
		driver.find_element_by_id('a3').click()
		sleep(0.3)
		driver.find_element_by_id('a34').click()
		sleep(0.3)
		driver.find_element_by_id('a108').click()
		sleep(0.3)
		driver.find_elements_by_css_selector('.bkdialog-footer > div > div')[0].click()
		driver.find_element_by_css_selector('#m18_bookname_td > div').send_keys(result['title'])  # 书名
		driver.find_element_by_css_selector('#m18_author_td > div').send_keys(result['author'])  # 作者
		driver.find_element_by_css_selector('#m18_isbn_td > div').send_keys(result['bar'][7][5:])  # ISBN
		driver.find_element_by_css_selector('#m18_price_td > div').send_keys(result['bar'][2][3:])  # 价格
		driver.find_element_by_css_selector('#m18_press_td > div').send_keys('中国人民大学出版社')  # 出版社
		driver.find_element_by_css_selector('#m18_t_td > div').send_keys(result['bar'][6][5:])  # 出版时间
		driver.find_element_by_css_selector('#m18_zz_td > div').send_keys(result['bar'][8][3:])  # 装帧
		driver.find_element_by_css_selector('#m18_kb_td > div').send_keys(result['bar'][5][3:])  # 开本
		# 一定要按pageup，让添加概述的按钮可见
		ActionChains(driver).key_down('\ue00e', element=None).key_up('\ue00e', element=None).perform()

	def add_content(self, driver, result):
		WebDriverWait(driver, 40, 0.5).until(EC.presence_of_element_located((By.ID, 'reference0')))

		refer = driver.find_element_by_css_selector('#reference0')
		ActionChains(driver).click(refer).key_down('\ue014', element=None).key_up('\ue014', element=None).perform()
		sleep(1)
		ActionChains(driver).click(refer).key_down('\ue014', element=None).key_up('\ue014', element=None).perform()
		sleep(1)
		ActionChains(driver).key_down('\ue00f', element=None).key_up('\ue00f', element=None).perform()
		sleep(1)
		ActionChains(driver).key_down('\ue00f', element=None).key_up('\ue00f', element=None).perform()
		sleep(1)
		ActionChains(driver).key_down('\ue007', element=None).key_up('\ue007', element=None).perform()
		sleep(1)

		# 输入作者简介
		if len(result['author_info']) > 10:
			ActionChains(driver).send_keys('作者简介').key_down(Keys.CONTROL, element=None).key_down('1',
			                                                                                     element=None).key_up(
				'1', element=None).key_up(Keys.CONTROL, element=None).perform()
			ActionChains(driver).key_down('\ue010', element=None).key_up('\ue010', element=None).key_down('\ue007',
			                                                                                              element=None).key_up(
				'\ue007', element=None).perform()
			sleep(1)
			ActionChains(driver).send_keys(result['author_info']).perform()
			sleep(2)

			# 切换到默认frame，添加参考资料
			driver.switch_to.default_content()
			driver.find_element_by_id('bke_reference').click()
			sleep(0.3)
			driver.find_element_by_id('reference-list-body').click()
			sleep(0.3)
			# 切换到编辑界面，换行
			driver.switch_to_frame('ueditor_0')
			ActionChains(driver).key_down('\ue010', element=None).key_up('\ue010', element=None).key_down('\ue007',
			                                                                                              element=None).key_up(
				'\ue007', element=None).perform()
			# 输入目录
			if len(result['directory']) > 20:
				ActionChains(driver).send_keys('目录').key_down(Keys.CONTROL, element=None).key_down('1',
				                                                                                   element=None).key_up(
					'1', element=None).key_up(Keys.CONTROL, element=None).perform()
				sleep(0.3)
				ActionChains(driver).key_down('\ue010', element=None).key_up('\ue010', element=None).key_down(
					'\ue007', element=None).key_up('\ue007', element=None).perform()
				ActionChains(driver).send_keys(result['directory']).perform()
				sleep(1)
				# 切换到默认frame
				driver.switch_to.default_content()
				# 提交参考资料
				driver.find_element_by_id('bke_reference').click()
				driver.find_element_by_id('reference-list-body').click()
				ActionChains(driver).key_down('\ue00e', element=None).key_up('\ue00e', element=None).perform()
				sleep(1)
				ActionChains(driver).key_down('\ue00e', element=None).key_up('\ue00e', element=None).perform()
				sleep(1)

			# 点击大的提交按钮
			click_element_big = driver.find_element_by_id('lemma-submit-btn-right')
			ActionChains(driver).move_to_element_with_offset(click_element_big, 65, 41).perform()
			driver.find_element_by_id('lemma-submit-btn-right').click()
			# 输入修改原因
			driver.find_element_by_id('dialogLemmaref').send_keys('基本信息栏 内容扩充 目录结构 参考资料 ')

			sleep(2)
			# 找到最终提交按钮(小)，并点击
			if result['down_url'] == '':
				driver.find_elements_by_css_selector('.bkdialog-footer > div >div')[0].click()
			else:
				driver.find_elements_by_css_selector('.bkdialog-footer > div >div')[2].click()

# def edit(self,baike,cookiestr,num):
# 	url = "http://baike.baidu.com/submitedit"
# 	title = parse.quote(baike['title'])
# 	ref = 'http://baike.baidu.com/edit/' + title +'/' +str(num)
# 	content_type = 'multipart/form-data; boundary='+baike['boundary']
# 	headers = {
# 		'Connection': 'keep-alive',
# 		'Cache-Control': 'max-age=0',
# 		'Origin': 'http://baike.baidu.com',
# 		'Upgrade-Insecure-Requests': '1',
# 		'Content-Type': content_type,
# 		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
# 		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 		'Referer': ref,
# 		'Accept-Encoding': 'gzip, deflate',
# 		'Accept-Language': 'zh-CN,zh;q=0.9',
# 		'Cookie': cookiestr
# 	}
# 	multipart_encoder = MultipartEncoder(
# 		fields={
# 			"preFlag":'',
# 			'from':'',
# 			'album': '',
# 			'video': '',
# 			'map': '',
# 			'abstract': '{"imgSrc":"","imgTitle":"","summaryContent":"<p>《' + baike['title'] + '》是2018年中国人民大学出版社出版书籍，作者是' + baike['author'] + '。</p>","width":"","height":"","picId":"","owner":""}',
# 			'moduleContent': '{"extAlbumData":{}}',
# 			'reference': '[{"type":1,"title":"' + baike['title'] + '","url":"' + baike['referance'] + '","site":"中国人民大学出版社","publishDate":"","refDate":"' + baike['date'] + '","index":1}]',
# 			'card': '{"type":"18","content":[{"key":"m18_bookname","name":"书名","value":["'+baike['title']+'"],"format":["'+baike['title']+'"]},{"key":"m18_author","name":"作者","value":["'+baike['author']+'"],"format":["'+baike['author']+'"]},{"key":"m18_isbn","name":"ISBN","value":["'+baike['bar'][7]+'"],"format":["'+baike['bar'][7]+'"]},{"key":"m18_price","name":"定价","value":["'+baike['bar'][2]+'"],"format":["'+baike['bar'][2]+'"]},{"key":"m18_press","name":"出版社","value":["中国人民大学出版社"],"format":["中国人民大学出版社"]},{"key":"m18_t","name":"出版时间","value":["'+baike['bar'][6]+'"],"format":["'+baike['bar'][6]+'"]},{"key":"m18_zz","name":"装帧","value":["平"],"format":["平"]},{"key":"m18_kb","name":"开本","value":["'+baike['bar'][5]+'"],"format":["'+baike['bar'][5]+'"]},{"key":"m18_ext_0","name":"印次","value":["'+baike['bar'][4]+'"],"format":["'+baike['bar'][4]+'"]},{"key":"m18_ext_1","name":"字数","value":["'+baike['bar'][3]+'"],"format":["'+baike['bar'][3]+'"]},{"key":"m18_ext_2","name":"书号","value":["'+baike['bar'][1]+'"],"format":["'+baike['bar'][1]+'"]}]}',
# 			'classify': 'a0,a3,a34,a108:文化_出版物_书籍',
# 			'draftId': '0',
# 			'draftType': '',
# 			'extAlbumData': 'false',
# 			'personal': 'null',
# 			'series': '',
# 			'tuwen': 'null',
# 			'music': '',
# 			'commonModuleList': '',
# 			'callback': 'POST_EDIT_CALLBACK',
# 			'lemmaTime': baike['lemmaTime'],
# 			'lemmaVersionId': '',
# 			'beforeLemma': '',
# 			'endLemma': '',
# 			'paragraphNum': '0',
# 			'lemmaTitle': baike['title'],
# 			'lemmaid': str(num),
# 			'extDataInit': '',
# 			'summaryImgIdInit': '',
# 			'summaryImgInfoInit': '',
# 			'summarySummaryInit': '<p></p>',
# 			'extDataTypeInit': '',
# 			'extDataTypeTempInit': '',
# 			'isCreate': '0',
# 			'isSectionEdit': '0',
# 			'referenceEdited':'0',
# 			'message': baike['message'],
# 			'lemmamodify': '内容扩充 目录结构 基本信息栏',
# 			'oriDesc': '',
# 			'subLemmaDesc': baike['title'],
# 			'createlemma': ' 提 交 ',
# 			'propsId': '',
# 			'propsClassId': '',
# 			'mc_al_name': '请输入专辑名称',
# 			'mc_al_date': '2011-03-04',
# 			'mc_al_lge': '国语',
# 			'mc_al_type': 'other',
# 			'mc_al_com': '',
# 			'mc_al_rec': '',
# 			'mc_al_userd_key_0': '',
# 			'mc_al_song_0': '',
# 			'title': '第1集',
# 			# 'editorValue': baike['editorValue']
# 		},
# 		boundary = baike['boundary']
# 	)
#
# 	r = requests.post(url, data=multipart_encoder, headers=headers)
# 	return r
