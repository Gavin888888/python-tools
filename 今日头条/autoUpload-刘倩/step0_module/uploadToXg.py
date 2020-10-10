from selenium import webdriver
import time
import json

br = webdriver.Chrome()
br.get("https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG")
with open('cookies.json') as f:
    cookies = json.loads(f.read())
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']

    br.add_cookie(cookie)

br.get("https://mp.toutiao.com/profile_v3/index")

time.sleep(3)
# 点击左侧导航栏 “西瓜视频”按钮
xigua_button = br.find_element_by_xpath(
    '//*[@id="root"]/div/div[2]/ul/li[2]/div/span')
xigua_button.click()
time.sleep(1)
# 点击左侧导航栏 “西瓜视频” --> “发布视屏”按钮
publish_vedio = br.find_element_by_xpath(
    '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[2]/a')
publish_vedio.click()
time.sleep(1)

upload_vedio = br.find_element_by_xpath(
    '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/input')
upload_vedio.send_keys(r'/Users/leili/Desktop/1.mp4')
time.sleep(2)
# 获取标题输入框，清除原标题并输入新标题
title_input = br.find_element_by_xpath(
    '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div/div/input')
title_input.clear()
title_input.send_keys('标题' * 3)

# 获得简介并输入内容
jianjie_textarea = br.find_element_by_xpath(
    '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[3]/div[2]/div/div/textarea')
jianjie_textarea.clear()
jianjie_textarea.send_keys('简介' * 5)

# # 获得是否投放广告
# toufang_radio = br.find_element_by_css_selector(
#     '#upload-manage > div > div.video-list-content > div > div.m-video-item > div.m-edit-from > div:nth-child(1) > div.m-form-item.m-ads > div > div.tui2-radio-group > label:nth-child(1)')
# toufang_radio.click()
#
# toufang_radio_no = br.find_element_by_css_selector(
#     '#upload-manage > div > div.video-list-content > div > div.m-video-item > div.m-edit-from > div:nth-child(1) > div.m-form-item.m-ads > div > div.tui2-radio-group > label:nth-child(2)')
# # toufang_radio_no.click()
#
#
# tag_name_html = '<div class="Select-value"><span class="Select-value-icon" aria-hidden="true">×</span><span class="Select-value-label" role="option" aria-selected="true" id="react-select-2--value-0">www<span class="Select-aria-only">&nbsp;</span></span></div>'
# # 添加视频标签
# # vedio_tags = br.find_element_by_id('react-select-2--value')
# tags_js = "document.getElementById('react-select-2--value').innerHTML=tag_name_html"
#br.execute_script(tags_js)
