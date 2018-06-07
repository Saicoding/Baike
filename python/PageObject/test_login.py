from LoginPage import  *
from selenium import  webdriver


driver=webdriver.Firefox()


username='root'
password='ty11202'
print('ok')
test_user_login(driver,username,password)
sleep(4)

driver.quit()