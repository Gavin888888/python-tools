import requests
import json
import shutil
import  os
import time
import random
from selenium import webdriver
import datetime

phones=["15611729727","13125005820","15801303573","13718665070","13129972887","18701233483"]

def sendMsg(msg):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=465e5a99c7a1857e07d29f004b977a291629f6c6a49da5f6f528ce181aa04be6'
    program = {
        "msgtype": "text",
        "text": {"content": "头条号 {}".format(msg)},
    }
    headers = {'Content-Type': 'application/json'}
    f = requests.post(url, data=json.dumps(program), headers=headers)
    print(f)

def getMsg(cookies_path):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    br = webdriver.Chrome(options=options)
    try:
        br.get("https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG")
        with open(cookies_path) as f:
            cookies = json.loads(f.read())
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']

            br.add_cookie(cookie)
        br.get("https://mp.toutiao.com/profile_v3/index")

        sleep_time = random.randint(5, 8)
        print("启动头条号 停顿：{}秒".format(sleep_time))
        time.sleep(sleep_time)

        # 点击左侧导航栏 “西瓜视频”按钮
        xigua_button = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/div/span')
        xigua_button.click()

        sleep_time = random.randint(3, 6)
        print("点击左侧导航栏 “西瓜视频”按钮 停顿：{}秒".format(sleep_time))
        time.sleep(sleep_time)

        # 点击左侧导航栏 “西瓜视频” --> “视频主页”按钮
        publish_vedio = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[1]/a')
        publish_vedio.click()

        sleep_time = random.randint(4, 6)
        print("点击左侧导航栏 “西瓜视频” --> “视频主页”按钮 停顿：{}秒".format(sleep_time))
        time.sleep(sleep_time)

        today_play_count_element = br.find_element_by_xpath(
            '//*[@id="xigua"]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/span[2]')
        today_play_count='{}'.format(str(today_play_count_element.text))

        time.sleep(2)

        today_income_element = br.find_element_by_xpath(
            '//*[@id="xigua"]/div/div/div[2]/div[1]/div[2]/div[2]/div/div/span[2]')
        today_income='{}'.format(str(today_income_element.text))

        time.sleep(2)

        all_income_element = br.find_element_by_xpath(
            '//*[@id="xigua"]/div/div/div[2]/div[1]/div[2]/a/span')
        all_income = '{}'.format(str(all_income_element.text))
        return today_play_count, today_income,all_income;
    except Exception as  error:
        print(error)


if __name__ == '__main__':
    print("启动钉钉机器人发送消息")
    today = (datetime.datetime.now()).strftime("%Y-%m-%d")
    all_income=0
    all_today_income = 0
    all_datas=[]
    for phone in phones:
        cookies_path = "{}/cookies/cookies_{}.json".format(os.path.abspath("."), phone)
        print(cookies_path)
        today_play_count,today_income,month_income=getMsg(cookies_path)
        all_msg = ":{}\n今日日期:{}\n今日收益:￥{} \n今日播放:{}\n视频总收益:{}".format(str(phone),str(today),str(today_income),str(today_play_count),str(month_income))
        if str(today_income).find('计算中') != 0:
            all_today_income+=float(today_income)
            all_income += float(month_income)
            all_datas.append(all_msg)
        else:
            all_income += 0
            all_today_income+= 0
    if len(all_datas) == len(phones):
        for i in all_datas:
            sendMsg(i)
        all_income_msg = ":%s\n今日总收益:￥%.2f\n视频总收益:￥%.2f"%(str(today),all_today_income,all_income)
        sendMsg(all_income_msg)
    exit()





