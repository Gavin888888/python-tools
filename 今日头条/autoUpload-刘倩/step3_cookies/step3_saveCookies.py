# 首次使用selenium登录，并将cookies存为文件

from selenium import webdriver
import time
import json

phone_number='15110230192'
auto_code='9436'

browser = webdriver.Chrome()
browser.get("https://mp.toutiao.com")

browser.find_element_by_id('sso_pwd_login').click()
time.sleep(3)

# 填写手机号
phone=browser.find_element_by_xpath('//*[@id="sso_container"]/div/div[1]/form/div[1]/div[2]/input')
phone.send_keys(phone_number)
time.sleep(1)

#验证码
# autoCode=browser.find_element_by_xpath('//*[@id="sso_container"]/div/div[1]/form/div[2]/input')
# autoCode.send_keys(auto_code)
# time.sleep(3)

# # 填写密码
password=browser.find_element_by_xpath("//*[@id='sso_container']/div/div[1]/form/div[2]/input")
password.send_keys('lsr2019')
time.sleep(3)
# 登陆
browser.find_element_by_xpath("//*[@id='sso_submit']").click()
time.sleep(5)
cookies = browser.get_cookies()
print(cookies)
with open('./cookies_{}.json'.format(phone_number), 'w') as f:
    self_cookies = f.write(json.dumps(cookies))
