from selenium.webdriver.common.by import By
from model import myunit
from page_object.trade_login import *
import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from search.search_funs import SearchFuns
from urllib import parse

#设置无头还是有头
myunit.StartEnd.headless = True

class SearchBaike(myunit.StartEnd):
    def test_login(self):
        # 设置定位器，登陆账号等信息
        options={
			'username': '欢乐麻酱',
			'password': 'ty11202',
			'base_url': 'https://passport.baidu.com/v2/?login',
			'username_loc': (By.ID, "TANGRAM__PSP_3__userName"),
			'password_loc': (By.ID, "TANGRAM__PSP_3__password"),
			'submit_loc': (By.ID, "TANGRAM__PSP_3__submit"),
			'pass_loc': (By.ID, "displayUsername"),
			'fail_loc': (By.ID, "TANGRAM__PSP_3__error"),
			'trade_loc': (By.ID, "TANGRAM__PSP_3__footerULoginBtn"),
			'url': ''}

        po = LoginBaike(self.driver, options)
        # 开始登陆
        po.login_action()
        # 验证是否登陆成功
        self.assertEqual(po.login_pass_hint(), po.options['username'])

        search_funs = SearchFuns()
        # 得到开始时间的int
        start_time = search_funs.get_start_time()

        # 得到开始num
        num = search_funs.get_ini('num')

        # 记录开始num，time以便统计
        start_statistics_num = num
        start_statistics_time = start_time

        # 尝试打开对应num的百科链接
        while True:
             # 判断是否中断循环,从run_test中引入mode, count_num两个变量
            if search_funs.decide_to_break("count", 16000, start_time):
                break
            # 得到pageNum
            page_num = search_funs.get_ini('pageNum')
            self.driver.get('http://baike.baidu.com/edit/1/'+num)
            # 设定等待时间
            time = 0
            while True:
                sleep(0.3)
                page_title = self.driver.title
                if time > 15:
                    self.driver.refresh()
                    time = 0
                if page_title != "":
                    break

                if time > 50:
                    search_funs.save_num()
                    num = int(num) + 1
                    num = str(num)
                    self.driver.get('http://baike.baidu.com/edit/1/' + num)
                    time = 0

                time += 1

            page_title = self.driver.title

            if ( page_title == "百度百科——全球最大中文百科全书" or page_title == "百度百科_全球最大中文百科全书"):
                search_funs.save_num()
                num = int(num) + 1
                num = str(num)
                self.driver.get('http://baike.baidu.com/edit/1/' + num)
            else:
                # 等待页面加载指定的元素出现
                WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'bke_title')))
                sleep(0.3)

                title = self.driver.find_element(By.ID, 'bke_title').text
                # 给词条名称做编码处理，不然phantomjs不识别中文网址
                title = parse.quote(title)
                # 打开历史版本
                self.driver.get('https://baike.baidu.com/historylist/' + title + '/' + num)
                while True:
                    sleep(0.3)
                    if self.driver.title !="" and self.driver.title == "百度百科——全球最大中文百科全书":
                        self.driver.get('https://baike.baidu.com/historylist/SO/18247')
                        break
                    else:
                        break

                    # 得到历史版本信息
                content = self.driver.find_element(By.TAG_NAME, 'tbody').text
                title = parse.unquote(title)
                title = title.replace("\"","\\\"")
                # 得到处理的字符串
                list_str = search_funs.get_list_str(content, title, num)
                # 处理字符串，并写入pageNum.json文件中
                search_funs.write_to_page_num(list_str, page_num)
                # 保存所有变化的量
                search_funs.save_data(start_statistics_num,start_statistics_time,list_str)
                # 统计各种数据
                search_funs.statistics(start_statistics_num, start_statistics_time,list_str)
                num = int(num) + 1
                num = str(num)


if __name__ == '__main__':
        unittest.main()
