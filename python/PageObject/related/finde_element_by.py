from selenium import  webdriver
from selenium.webdriver.common.by import  By
from time import  sleep

driver=webdriver.Firefox()
driver.get("http://www.baidu.com/")
driver.implicitly_wait(5)

driver.find_element(By.ID,'kw').clear()
driver.find_element(By.NAME,'wd').send_keys("性感")
driver.find_element(By.CLASS_NAME,'s_ipt').send_keys("大屁股")
driver.find_element(By.CSS_SELECTOR,'#kw').send_keys("大胸部")

sleep(3)
driver.find_element(By.ID,'su').click()