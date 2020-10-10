# -*- coding: utf-8 -*-
import schedule
import time
import datetime
import shutil
import os
import random
import requests
import json
import random
from selenium import webdriver
from mysql import DbManager


today = (datetime.datetime.now()).strftime("%Y-%m-%d")

def createTime(t1,t2):
    random_count = random.randint(t1, t2)
    time_h = "01"
    if random_count < 10:
        time_h = "0{}".format(str(random_count))
    else:
        time_h = "{}".format(str(random_count))
    will_pushlist_time = "{}:{}".format(time_h, str(random.randint(10, 60)))
    return will_pushlist_time

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
#
income_phones=["15611729727","13125005820","15801303573","13718665070","15110230192","13129972887","18701233483"]
def sendMsgJob():
    global today
    global income_phones

    # 范围时间
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '12:00', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '22:05', '%Y-%m-%d%H:%M')
    # 当前时间
    n_time = datetime.datetime.now()
    # 判断当前时间是否在范围时间内
    if n_time > start_time and n_time < end_time:
        if today == (datetime.datetime.now()).strftime("%Y-%m-%d"):
            print("启动钉钉机器人发送消息")
            all_income = 0
            all_today_income = 0
            all_datas = []
            for phone in income_phones:
                cookies_path = "{}/cookies/cookies_{}.json".format(os.path.abspath("."), phone)
                print(cookies_path)
                today_play_count, today_income, month_income = getMsg(cookies_path)
                all_msg = ":{}\n今日日期:{}\n今日收益:￥{} \n今日播放:{}\n视频总收益:￥{}".format(str(phone), str(today), str(today_income),
                                                                              str(today_play_count), str(month_income))
                if str(today_income).find('计算中') != 0:
                    all_today_income += float(today_income)
                    all_income += float(month_income)
                    all_datas.append(all_msg)
                else:
                    all_income += 0
                    all_today_income += 0
            if len(all_datas) == len(income_phones):
                for i in all_datas:
                    sendMsg(i)
                all_income_msg = ":%s\n今日总收益:￥%.2f\n视频总收益:￥%.2f" % (str(today), all_today_income, all_income)
                sendMsg(all_income_msg)
                tomorrow = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
                today = tomorrow
        else:
            print("今日收入数据已发，请等待 {} 数据".format(today))
    else:
        print("不在查询时间内，请等待 {} 至 {} 时间段内查询".format(start_time,end_time))
def publish_job():
    print('Job:开始分配今日任务  %s'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    global phones
    index=0
    for i in phones:
        index += 1
        if index==1:
            will_pushlist_time=createTime(3,4)
            print("头条号:{} 将在:{} 发布视频".format(i,will_pushlist_time))
            schedule.every().day.at(will_pushlist_time).do(job1)
        if index == 2:
            will_pushlist_time=createTime(5,6)
            print("头条号:{} 将在:{} 发布视频".format(i, will_pushlist_time))
            schedule.every().day.at(will_pushlist_time).do(job2)
        if index == 3:
            will_pushlist_time=createTime(7,8)
            print("头条号:{} 将在:{} 发布视频".format(i, will_pushlist_time))
            schedule.every().day.at(will_pushlist_time).do(job3)
        if index == 4:
            will_pushlist_time=createTime(9,10)
            print("头条号:{} 将在:{} 发布视频".format(i, will_pushlist_time))
            schedule.every().day.at(will_pushlist_time).do(job4)

    print('------------------------------------------------------------------------')
def job1():
    phone="15611729727"
    print('download_video_job--->%s开始' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    download_cmd = "python3 {}/scrapyiqy.py {}".format(os.path.abspath("."), phone)
    os.system(download_cmd)
    print("下载任务完成 等待发布任务")
    publish_cmd="python3 {}/push2xgsp.py {}".format(os.path.abspath("."),phone)
    print(publish_cmd)
    os.system(publish_cmd)

def job6():
    phone="13718665070"
    path="{}/download_videos/videos_{}".format(os.path.abspath("."), phone)
    path = path.strip().rstrip('\\')
    is_exists = os.path.exists(path)
    if not is_exists:  # 校验目录是否存在
        os.makedirs(path)
        print('创建媒体目录')
    else:
        print('媒体目录已经存在')
    new_path="/Volumes/lilei/项目/python/autoUpload/step4_allVideos/video_13718665070"
    files = [f for f in os.listdir(new_path) if not f.startswith('.')]

    will_push_files = [f for f in os.listdir(path) if not f.startswith('.')]
    print("还有{}条数据".format(len(will_push_files)))
    if len(will_push_files) == 0:
        index = 0
        for f in files:
            if index < 5:
                shutil.copy('{}'.format(new_path + "/" + f), '{}'.format(path + "/" + f))  # copy file
                os.remove(new_path + "/" + f)
            index += 1

    publish_cmd = "python3 {}/push2xgsp.py {}".format(os.path.abspath("."), phone)
    os.system(publish_cmd)

def download_video_job():
    print('download_video_job--->%s开始' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    for phone in phones:
        download_cmd = "python3 {}/scrapyiqy.py {}".format(os.path.abspath("."), phone)
        os.system(download_cmd)
    print("下载任务完成 等待发布任务")


#
phones=["15611729727","13129972887", "13125005820","15801303573"]
def all_step_job():
    # sendMsgJob()
    for phone in phones:
        video_path = "{}/download_videos/videos_{}".format(os.path.abspath("."), phone)
        files = [f for f in os.listdir(video_path) if not f.startswith('.')]
        if len(files) == 0:
            # 下载任务
            download_cmd = "python3 {}/scrapyiqy.py {}".format(os.path.abspath("."), phone)
            os.system(download_cmd)
        # 发布任务
        publish_cmd = "python3 {}/push2xgsp.py {}".format(os.path.abspath("."), phone)
        os.system(publish_cmd)

def lookmoney():
    for phone in income_phones:
        # 发布任务
        publish_cmd = "python3 {}/test.py {}".format(os.path.abspath("."), phone)
        os.system(publish_cmd)

if __name__ == '__main__':
    print("程序启动")
    lookmoney()
    # schedule.every(66).to(88).seconds.do(all_step_job)
    # while True:
    #     schedule.run_pending()
