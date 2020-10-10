# -*- coding: utf-8 -*-
import shutil
import  os
import json
import time
import random
from selenium import webdriver

phone="13125005820"
# phone="13129972887"
#phone="13718665070"
phone="15611729727"#
video_cookies="cookies_{}".format(phone)
video_type="video_{}".format(phone)
video_dict = "{}/step4_allVideos/{}".format(os.path.dirname(__file__),video_type)
br = webdriver.Chrome()

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


def getAllVideos(videopath):
    files = [f for f in os.listdir(videopath) if not f.startswith('.')]
    return files

def openTTH():
    br.get("https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG")
    with open('./step3_cookies/{}.json'.format(video_cookies)) as f:
        cookies = json.loads(f.read())
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']

        br.add_cookie(cookie)

    br.get("https://mp.toutiao.com/profile_v3/index")
    sleep_time = random.randint(5, 8)
    print("停顿：{}秒".format(sleep_time))
    time.sleep(sleep_time)
    try:
        # 点击左侧导航栏 “西瓜视频”按钮
        xigua_button = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/div/span')
        xigua_button.click()
    except Exception as  error:
        # 点击左侧导航栏 “西瓜视频”按钮
        xigua_button = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/div/span')
        xigua_button.click()


    try:
        sleep_time = random.randint(4, 10)
        print("停顿：{}秒".format(sleep_time))
        time.sleep(sleep_time)
        # 点击左侧导航栏 “西瓜视频” --> “发布视屏”按钮
        publish_vedio = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[2]/a')
        publish_vedio.click()
    except Exception as  error:
        sleep_time = random.randint(1, 10)
        print("停顿：{}秒".format(sleep_time))
        time.sleep(sleep_time)
        # 点击左侧导航栏 “西瓜视频” --> “发布视屏”按钮
        publish_vedio = br.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[2]/a')
        publish_vedio.click()

#上传视频
def uploadVideo():
    # 准备要发布的视频
    videos = getAllVideos(video_dict)
    for i in range(len(videos)):
        videoName = videos[i]
        videoPath = video_dict + "/" + videos[i]
        #视频名字
        if len(videoName) < 5 :
            videoName="   {}   ".format(videoName)
        if len(videoName) > 34 :
            video_type_list=videoName.split(".")
            videoName="{}.{}".format(videoName[:30],video_type_list[1])
            des_path = "{}/{}".format(video_dict, videoName)
            os.rename(videoPath, des_path)
            videoPath=des_path
        sleep_time = random.randint(5, 10)
        mod_print("开始发布视频：{}秒".format(sleep_time), ANSI_GREEN, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)

        time.sleep(sleep_time)

        mod_print("视频名字：{} \n视频路径：{}".format(videoName, videoPath), ANSI_YELLOW, ANSI_BLACK_BACKGROUND, MOD_UNDERLINE)
        try:
            upload_video = br.find_element_by_xpath(
                '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/input')
            upload_video.send_keys(r'{}'.format(videoPath))
        except Exception as  error:
            mod_print(error, ANSI_RED, ANSI_WHITE_BACKGROUND, MOD_UNDERLINE)
            restart()

        sleep_time = random.randint(3, 10)
        print("停顿：{}秒".format(sleep_time))
        time.sleep(sleep_time)

        # upload_percent = br.find_element_by_xpath('//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div').get_attribute("style")
        # print(upload_percent)
        runloop = True
        while runloop:
            try:
                width_percent = br.find_element_by_xpath(
                    '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div')
                percent = width_percent.value_of_css_property("width")
                print("文件上传：", percent)
                time.sleep(1)
                if percent == "884px":
                    runloop = False

                    sleep_time = random.randint(5, 10)
                    print("停顿{}秒加载封面".format(sleep_time))
                    time.sleep(sleep_time)

                    # 上传完毕后 点击 发布按钮
                    publist_btn = br.find_element_by_xpath(
                        '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[3]/button[4]')
                    publist_btn.click()
                    # 上传完毕 把文件删除
                    if (os.path.exists(videoPath)):
                        os.remove(videoPath)
                        mod_print("{}--->已删除".format(videoPath), ANSI_RED, ANSI_WHITE_BACKGROUND, MOD_UNDERLINE)

                    sleep_time = random.randint(5, 10)
                    print("发布完成休息{}秒".format(sleep_time))
                    time.sleep(sleep_time)

                    # 点击左侧导航栏 “西瓜视频” --> “发布视屏”按钮
                    publish_vedio = br.find_element_by_xpath(
                        '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[2]/a')
                    publish_vedio.click()

            except Exception as  error:
                mod_print(error, ANSI_RED, ANSI_WHITE_BACKGROUND, MOD_UNDERLINE)
                restart()


#出现异常重新开始
def restart():
    print("出现异常重新开始")
    # 打开头条号 并到发布视频页面
    openTTH()
    # 开始上传
    uploadVideo()

if __name__ == "__main__":
    print("程序开始")
    #打开头条号 并到发布视频页面
    openTTH()
    #开始上传
    # uploadVideo()
    # #执行完毕退出
    # br.quit()



        # # 获取标题输入框，清除原标题并输入新标题
        # title_input = br.find_element_by_xpath(
        #     '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div/div/input')
        # title_input.clear()
        # title_input.send_keys(videoName)
        #
        # sleep_time = random.randint(0, 10)
        # print("停顿：{}秒".format(sleep_time))
        # time.sleep(sleep_time)
        #
        # # 获得简介并输入内容
        # jianjie_textarea = br.find_element_by_xpath(
        #     '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[3]/div[2]/div/div/textarea')
        # jianjie_textarea.clear()
        # jianjie_textarea.send_keys(videoName)