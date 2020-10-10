# -*- coding: utf-8 -*-
import schedule
import time
import datetime
import shutil
import os
import json
import random
from step2_dbmanager.mysql import DbManager
from selenium import webdriver

phone="13125005820"
# phone="13129972887"
# phone="15611729727"
# phone="13718665070"
video_type="video_{}".format(phone)
video_cookies="cookies_{}".format(phone)
will_pushlist_time="00:00" #默认 00：00 开发发布
will_publist_videos=[]
reload_counts=5

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
br = webdriver.Chrome()
dbmanager = DbManager()

ANSI_BLACK = 30
ANSI_RED = 31
ANSI_GREEN = 32
ANSI_YELLOW = 33
ANSI_BLUE = 34
ANSI_PURPLE = 35
ANSI_CYAN = 36
ANSI_WHITE = 37

ANSI_BLACK_BACKGROUND = 40
ANSI_RED_BACKGROUND = 41
ANSI_GREEN_BACKGROUND = 42
ANSI_YELLOW_BACKGROUND = 43
ANSI_BLUE_BACKGROUND = 44
ANSI_PURPLE_BACKGROUND = 45
ANSI_CYAN_BACKGROUND = 46
ANSI_WHITE_BACKGROUND = 47

MOD_DEFAULT = 0
MOD_HIGHLIGHT = 1
MOD_UNDERLINE = 4
MOD_FLICKER = 5
MOD_INVERSE = 7
MOD_HIDE = 8

def mod_print(message, fg=ANSI_WHITE, bg=ANSI_BLACK_BACKGROUND, mod=MOD_DEFAULT):
    """
    格式化输出
    :param message:
    :param fg:
    :param bg:
    :param mod:
    :return:
    """
    print('\033[{};{};{}m'.format(fg, bg, mod) + message + '\033[0m')

def getDataJob():
    print('设置任务-startTime:%s' %(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    pushlist_date = '%s' %(datetime.datetime.now().strftime('%Y-%m-%d'))
    sql="select * from {} where publish_time='{}' and publish_status=0;".format(video_type,pushlist_date)
    res=dbmanager.fetchall(sql)
    global will_publist_videos
    will_publist_videos=res
    random_count=random.randint(0, 22)
    time_h ="01"
    if random_count < 10:
        time_h="0{}".format(str(random_count))
    else:
        time_h = "{}".format(str(random_count))
    will_pushlist_time = "{}:{}".format(time_h, str(random.randint(10, 60)))


    #模拟
    will_pushlist_time='18:12'

    mod_print("将在{}发布以下数据".format(will_pushlist_time), ANSI_PURPLE, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)
    for tempVideo in will_publist_videos:
        mod_print("{}\t".format(tempVideo["id"]), ANSI_BLUE, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)

    schedule.every().day.at(will_pushlist_time).do(publishJob)

    print('设置任务-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

def publishJob():
    print('上传任务-startTime:%s' %(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    try:

        # 打开头条号 并到发布视频页面
        br.get("https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG")
        with open('./step3_cookies/{}.json'.format(video_cookies)) as f:
            cookies = json.loads(f.read())
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']

            br.add_cookie(cookie)
        br.get("https://mp.toutiao.com/profile_v3/index")
        sleep_time = random.randint(100, 100)
        print("打开网页：停顿{}秒".format(sleep_time))
        time.sleep(sleep_time)
        
        # 点击左侧导航栏 “西瓜视频”按钮
        xigua_button = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/div/span')
        xigua_button.click()
        sleep_time = random.randint(1, 10)
        print("点击左侧导航栏 “西瓜视频”按钮：停顿{}秒".format(sleep_time))
        time.sleep(sleep_time)
        # 点击左侧导航栏 “西瓜视频” --> “发布视屏”按钮
        publish_vedio = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[2]/a')
        publish_vedio.click()
        sleep_time = random.randint(1, 10)
        print("点击左侧导航栏 “西瓜视频” -> “发布视屏”按钮：停顿{}秒".format(sleep_time))

        global will_publist_videos
        # 开始上传
        videos = will_publist_videos
        print(videos)
        # 记录发布一条视频的时间

        for tempVideo in videos:
            push_one_video_time = 0
            sleep_time = random.randint(5, 10)
            time.sleep(sleep_time)
            mod_print("开始发布视频：停顿{}秒".format(sleep_time), ANSI_GREEN, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)

            videoID = tempVideo["id"]
            videoName = tempVideo["title"]
            videoPath = tempVideo["local_path"]
            mod_print("视频名字：{} \n视频路径：{}".format(videoName, videoPath), ANSI_YELLOW, ANSI_BLACK_BACKGROUND,
                      MOD_UNDERLINE)
            try:
                upload_video = br.find_element_by_xpath(
                    '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/input')
                upload_video.send_keys(r'{}'.format(videoPath))
            except Exception as  error:
                print(error)
                # # br退出
                # br.quit()
                # # 重新开始
                # restart()

            # sleep_time = random.randint(3, 10)
            # time.sleep(sleep_time)
            # mod_print("视频正在上传：停顿{}秒".format(sleep_time), ANSI_GREEN, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)

            runloop = True
            while runloop:
                try:
                    width_percent = br.find_element_by_xpath(
                        '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div')
                    percent = width_percent.value_of_css_property("width")
                    all_width = "884px"

                    # uploaded_width = int(percent.replace("px", ""))
                    # print(uploaded_width)
                    #
                    # all_width_number = int(all_width.replace("px", ""))
                    # percentStr = '%.2f' % (uploaded_width / all_width_number)
                    # ppp = int(float(percentStr) * 100)
                    print("文件已上传：{}={}>".format(percent, all_width))

                    if percent == all_width:
                        runloop = False
                        sleep_time = random.randint(5, 10)
                        time.sleep(sleep_time)
                        mod_print("视频已经上传完成：停顿{}秒加载封面".format(sleep_time), ANSI_GREEN, ANSI_BLACK_BACKGROUND,
                                  MOD_UNDERLINE)

                        # 上传完毕后 点击 发布按钮
                        publist_btn = br.find_element_by_xpath(
                            '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[3]/button[4]')
                        publist_btn.click()
                        mod_print("上传完毕后 点击 发布按钮", ANSI_GREEN, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)

                        sleep_time = random.randint(5, 10)
                        mod_print("发布完成：停顿{}秒".format(sleep_time), ANSI_GREEN, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)
                        time.sleep(sleep_time)

                        # 点击左侧导航栏 “西瓜视频” --> “发布视频”按钮
                        publish_vedio = br.find_element_by_xpath(
                            '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[2]/a')
                        publish_vedio.click()
                        mod_print("点击左侧导航栏 “西瓜视频” --> “发布视频”按钮", ANSI_GREEN, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)

                        # 更新视频上传状态
                        releasetime = '%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        sql_update = 'UPDATE {} SET release_time = "{}",publish_status = 1 WHERE id = "{}"'.format(
                            video_type, releasetime, videoID)
                        print("更新状态sql:{}".format(sql_update))
                        dbmanager.edit(sql_update)

                except Exception as  error:
                    # br退出
                    br.quit()
                    # 重新开始
                    restart()

        # 执行完毕退出
        br.quit()
    except Exception as  error:
        print(error)
        # br退出
        br.quit()
        # 重新开始
        restart()
    print('上传任务-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

#出现异常重新开始
def restart():
    global reload_counts
    if reload_counts == 0:
        mod_print("出现异常重新开始", ANSI_RED, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)
        # 重新开始
        pushlist_date = '%s' % (datetime.datetime.now().strftime('%Y-%m-%d'))
        sql = "select * from {} where publish_time='{}' and publish_status=0;".format(video_type, pushlist_date)
        res = dbmanager.fetchall(sql)
        global will_publist_videos
        will_publist_videos = res
        publishJob()
        reload_counts-=1

if __name__ == '__main__':
    # schedule.every().day.at('14:50').do(getDataJob)


    getDataJob()
    # time.sleep(3)
    # publishJob()

    while True:
        schedule.run_pending()