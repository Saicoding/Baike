# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
from time import sleep
from model.myclass import TaskbarIcon


# 保存快照
def insert_img(driver, filename):
	# 在哪里调用这个方法，就返回该方法文件所在的目录
	func_path = os.path.dirname(__file__)

	# 获得上一级目录
	base_dir = os.path.dirname(func_path)

	# 把路径换成字符串，并把‘\’转为‘/’
	base_dir = str(base_dir)
	base_dir = base_dir.replace('\\', '/')

	# 把路径以‘/website'为分割点分离
	base = base_dir.split('/website')[0]

	filepath = base + '/website/test_report/screenshot/' + filename
	print(filepath)
	driver.get_screenshot_as_file(filepath)


# 发送邮件

def send_mail(latest_report):
	f = open(latest_report, 'rb')
	content = f.read()
	f.close()

	smtpserver = 'smtp.163.com'

	user = 'tyyx11202@163.com'
	password = 'ty8399782'

	sender = user
	receivers = ['tyyx11202@gmail.com', '417353147@qq.com']

	subject = '第二封自动邮件'

	msg = MIMEText(content, 'html', 'utf-8')
	msg['Subject'] = Header(subject, 'utf-8')
	msg['From'] = sender
	msg['To'] = ','.join(receivers)

	smtp = smtplib.SMTP_SSL(smtpserver, 465)
	smtp.helo(smtpserver)
	smtp.ehlo(smtpserver)
	smtp.login(user, password)
	print('发送邮件')
	smtp.sendmail(sender, receivers, msg.as_string())
	smtp.quit()
	print('发送成功')


def send_statics_email(info):
	smtpserver = 'smtp.163.com'

	user = 'tyyx11202@163.com'
	password = 'ty8399782'

	sender = user
	receivers = ['tyyx11202@gmail.com', '417353147@qq.com']

	subject = '过去一天的百科统计'

	msg = MIMEText(info, 'html', 'utf-8')
	msg['Subject'] = Header(subject, 'utf-8')
	msg['From'] = sender
	msg['To'] = ','.join(receivers)

	smtp = smtplib.SMTP_SSL(smtpserver, 465)
	smtp.helo(smtpserver)
	smtp.ehlo(smtpserver)
	smtp.login(user, password)

	print('发送邮件')
	smtp.sendmail(sender, receivers, msg.as_string())
	smtp.quit()
	print('发送成功')


# 发送报告
def latest_report(report_dir):
	lists = os.listdir(report_dir)
	lists.sort(key=lambda fn: os.path.getatime(report_dir + '\\' + fn))
	file = os.path.join(report_dir, lists[-1])
	return file


# 把类先声明出来放到程序最开始的地方，以免重复
bar_pop = TaskbarIcon()


# 系统任务栏pop
def pop(bar_pop, msg):
	title = ''
	if msg[0] == 0:
		title = '创建词条'
	elif msg[0] == 1:
		title = '编辑词条'
	elif msg[0] == 2:
		title = '搜索词条'
	elif msg[0] == 3:
		title = '账号监控'
	bar_pop.showMsg(title, msg[1])
	sleep(5)
# 启用就会出错
# win32gui.DestroyWindow(bar_pop.hwnd)
