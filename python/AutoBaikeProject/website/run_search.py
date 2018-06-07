import unittest
from test_case.model.function import *
from BSTestRunner import BSTestRunner
import time


report_dir = './test_report'
test_dir = './test_case'

print('开始测试')
discover = unittest.defaultTestLoader.discover(test_dir,pattern="search_baike.py")

now=time.strftime("%Y-%m-%d %H_%M_%S")
report_name = report_dir + '/'+now+'result.html'

print('开始写报告')
with open(report_name, 'wb') as f:
	runner = BSTestRunner(stream=f, title="百科查询报告", description="")
	runner.run(discover)
	f.close()
'--load-images=false'
print("寻找最新报告")
latest_report = latest_report(report_dir)

print("发最新报告到邮件")
send_mail(latest_report)

print("测试结束")

