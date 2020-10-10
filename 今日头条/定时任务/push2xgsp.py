# -*- coding: utf-8 -*-
import shutil
import  os
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
from mysql import DbManager
import datetime


# print('参数个数为:', len(sys.argv), '个参数。')
# print('参数列表:', str(sys.argv))
phone=str(sys.argv[1])

video_cookies="{}/cookies/cookies_{}.json".format(os.path.abspath("."),phone)
video_dict = "{}/download_videos/videos_{}".format(os.path.abspath("."), phone)

exception_count=0

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito') # 隐身模式（无痕模式）

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

user_agent=random.choice(USER_AGENTS)
print("*"*100)
print(user_agent)
chrome_options.add_argument(
    'user-agent={}'.format(user_agent))
# 设置代理
proxy_servers=["http://117.131.119.116:80"]
proxy_server=random.choice(proxy_servers)
# chrome_options.add_argument("--proxy-server={}".format(proxy_server))

br = webdriver.Chrome(options=chrome_options)

# 查看本机ip，查看代理是否起作用
# br.get("http://httpbin.org/ip")
print(proxy_server)
print("*"*100)

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

def mod_print(message, fg=ANSI_WHITE, mod=MOD_DEFAULT):
    """
    格式化输出
    :param message:
    :param fg:
    :param mod:
    :return:
    """
    print('\033[{};{}m'.format(fg, mod) + message + '\033[0m')


def getAllVideos(videopath):
    files = [f for f in os.listdir(videopath) if not f.startswith('.')]
    return files

def openTTH():
    br.get("https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG")
    with open(video_cookies) as f:
        cookies = json.loads(f.read())
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        br.add_cookie(cookie)

    br.get("https://mp.toutiao.com/profile_v3/index")
    sleep_time = random.randint(10, 15)
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
        sleep_time = random.randint(10, 15)
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

        video_count = len(getAllVideos(video_dict))
        mod_print("还有：{}条视频".format(str(video_count)), ANSI_PURPLE, MOD_UNDERLINE)
        if video_count == 0:
            # 执行完毕退出
            br.quit()
            sys.exit(0)
            return

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
        mod_print("开始发布视频：停顿{}秒".format(sleep_time), ANSI_GREEN, MOD_UNDERLINE)

        time.sleep(sleep_time)

        mod_print("视频名字：{} \n视频路径：{}".format(videoName, videoPath), ANSI_YELLOW, MOD_UNDERLINE)
        try:
            upload_video = br.find_element_by_xpath(
                '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/input')
            upload_video.send_keys(r'{}'.format(videoPath))
        except Exception as  error:
            restart(error)

        sleep_time = random.randint(3, 10)
        print("停顿：{}秒".format(sleep_time))
        time.sleep(sleep_time)

        # upload_percent = br.find_element_by_xpath('//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div').get_attribute("style")
        # print(upload_percent)



        # # 添加标签
        #
        # br.find_element_by_xpath(
        #     '//*[@id="xigua"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div').click()
        # video_tag = br.find_element_by_xpath(
        #     '//*[@id="xigua"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div/div/ul/li/input')
        # print(video_tag)
        # video_tag.send_keys('{}'.format("ssssdddd"))
        # video_tag.send_keys(Keys.ENTER)
        # return


        runloop = True
        runloop_count=0
        while runloop:
            time.sleep(1)
            runloop_count+=1
            if runloop > 60*10:
                # 执行完毕退出
                br.quit()
                sys.exit(0)

            try:
                width_percent = br.find_element_by_xpath(
                    '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div')
                percent = width_percent.value_of_css_property("width")
                print("文件上传：", percent)
                time.sleep(1)
                if percent == "884px":
                    runloop = False

                    print("停顿20秒加载封面")
                    time.sleep(20)

                    # try:
                    #     # 选择第二个当封面
                    #     cover_btn = br.find_element_by_xpath(
                    #         '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/img')
                    #     cover_btn.click()
                    # except Exception as  error:
                    #     print(error)
                    #     print("再停顿20秒加载封面")
                    #     time.sleep(20)
                    #     # 选择第二个当封面
                    #     cover_btn = br.find_element_by_xpath(
                    #         '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/img')
                    #     cover_btn.click()
                    #
                    # print("停顿5秒点击")
                    # time.sleep(5)


                    # 上传完毕后 点击 发布按钮
                    publist_btn = br.find_element_by_xpath(
                        '//*[@id="xigua"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[3]/button[4]')
                    publist_btn.click()
                    # 上传完毕 把文件删除
                    if (os.path.exists(videoPath)):
                        os.remove(videoPath)
                        mod_print("{}--->已删除".format(videoPath), ANSI_RED, MOD_UNDERLINE)

                        video_title = videoName.replace(".mp4", "")
                        sql_update = "UPDATE iqy{} SET publish_status = 1,publish_time = '{}' WHERE title like '{}%';".format(phone,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                                                      video_title)
                        print(sql_update)
                        dbManager = DbManager()
                        res = dbManager.edit(sql_update)
                        print(res)
                    sleep_time = random.randint(5, 10)
                    print("发布完成休息{}秒".format(sleep_time))
                    time.sleep(sleep_time)

                    # 点击左侧导航栏 “西瓜视频” --> “发布视屏”按钮
                    publish_vedio = br.find_element_by_xpath(
                        '//*[@id="root"]/div/div[2]/ul/li[2]/ul/li[2]/a')
                    publish_vedio.click()

            except Exception as  error:
                restart(error)


#出现异常重新开始
def restart(error):
    video_count = len(getAllVideos(video_dict))
    mod_print("还有：{}条视频".format(str(video_count)), ANSI_PURPLE, MOD_UNDERLINE)
    if video_count == 0:
        # 执行完毕退出
        br.quit()
        sys.exit(0)
        return


    global exception_count

    print("出现{}次异常重新开始".format(str(exception_count)))
    print("-"*100)
    print(error)
    print("-" * 100)
    exception_count+=1
    if exception_count == 6:
        br.quit()
        sys.exit(0)
        return
    # 打开头条号 并到发布视频页面
    openTTH()
    # 开始上传
    uploadVideo()

if __name__ == "__main__":
    print("push2xgsp程序已启动，开始获取 {} 所需的数据".format(phone))
    videos = getAllVideos(video_dict)
    print("还有{}条视频".format(str(len(videos))))
    if len(videos) == 0:
        br.quit()
        sys.exit(0)
    else:
        # 打开头条号 并到发布视频页面
        openTTH()
        # 开始上传
        uploadVideo()
        # 执行完毕退出
        br.quit()




