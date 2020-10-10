# -*- coding: utf-8 -*-
import shutil
import  os
import json
import time
import datetime
import shutil
import random
import schedule
from selenium import webdriver
import asyncio
import tqdm
import subprocess
import sys
from mysql import DbManager

# print('参数个数为:', len(sys.argv), '个参数。')
# print('参数列表:', str(sys.argv))
phone=str(sys.argv[1])

video_path = "{}/download_videos/videos_{}".format(os.path.abspath("."), phone)
yestday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
today = (datetime.datetime.now()).strftime("%Y-%m-%d")

def getAllVideos(videopath):
    files = [f for f in os.listdir(videopath) if not f.startswith('.')]
    return files

def mkdir(path):
    path = path.strip().rstrip('\\')
    is_exists = os.path.exists(path)
    if not is_exists:  # 校验目录是否存在
        os.makedirs(path)
        print('创建媒体目录')
    else:
        print('媒体目录已经存在')
    return path + '/'


def getCanUseVideo(href):
    global canUseCount
    global video_path
    canUseCount=0
    videos=getAllVideos(video_path)
    for video in videos:
        video_absolut_path="{}/{}".format(video_path,video)
        size = get_FileSize(video_absolut_path)
        # print("%s 文件大小：%.2f MB" % (video,size))
        if size==0:
            os.remove(video_absolut_path)
        else:
            canUseCount+=1

    print("已下载可用的文件个数：%d" % (canUseCount))
    return canUseCount

def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)

def push_job():
    publish_cmd = "python3 {}/{}/{}".format(os.path.abspath("."), phone, "push2xgsp.py")
    os.system(publish_cmd)

def scrapy_youku(youku_urls):
    # 配置
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    videolist = []
    today_video_count = 0
    for url in youku_urls:
        print("获取该页面内容：{}".format(url))
        driver.get(url)
        href_xpath='/html/body/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/div[*]/div[3]/div[1]/a'
        title_xpath = '/html/body/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/div[*]/div[3]/div[1]/a'
        sub_date_xpath = '/html/body/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/div[*]/div[3]/div[2]/span'

        hrefs = driver.find_elements_by_xpath(href_xpath)
        titles = driver.find_elements_by_xpath(title_xpath)
        sub_dates = driver.find_elements_by_xpath(sub_date_xpath)
        print("页面上所有的条数：{}".format(str(len(hrefs))))
        index = 0
        for object in hrefs:
            href = hrefs[index].get_attribute('href')
            title = titles[index].text
            sub_date = sub_dates[index].text
            if "小时" in sub_date:
                today_video_count += 1
                # print("第" + str(today_video_count) + "条 " + sub_date + "   " + title + "   " + href)
                videoDictionary = {"title": title, "href": href, "sub_date": sub_date}
                videolist.append(videoDictionary)
            elif "分钟" in sub_date:
                today_video_count += 1
                # print("第" + str(today_video_count) + "条 " + sub_date + "   " + title + "   " + href)
                videoDictionary = {"title": title, "href": href, "sub_date": sub_date}
                videolist.append(videoDictionary)

            index+=1

    print("页面上当天的条数：{}".format(str(len(videolist))))
    driver.quit()
    if len(videolist) == 0:
        sys.exit(0)
    return videolist

def scrapy_iqy(iqy_urls):
    # 配置
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # 启动浏览器
    driver = webdriver.Chrome(options=options)

    videolist = []
    for url in iqy_urls:
        print("获取该页面内容：{}".format(url))
        driver.get(url)
        href_xpath = '//*[@id="block-D"]/ul/li[*]/div/div[1]/a'
        title_xpath = '//*[@id="block-D"]/ul/li[*]/div/div[2]/p[1]/a/span'
        sub_date_xpath = '//*[@id="block-D"]/ul/li[*]/div/div[2]/p[2]'

        hrefs = driver.find_elements_by_xpath(href_xpath)
        titles = driver.find_elements_by_xpath(title_xpath)
        sub_dates = driver.find_elements_by_xpath(sub_date_xpath)
        index = 0
        print("页面上所有的条数：{}".format(str(len(hrefs))))
        for object in hrefs:
            href = hrefs[index].get_attribute('href')
            title = titles[index].text
            sub_date = sub_dates[index].text
            # print(sub_date + "   " + title + "   " + href)
            if sub_date == today:
                videoDictionary = {"title": title, "href": href, "sub_date": sub_date}
                videolist.append(videoDictionary)
            index += 1
    print("页面上当天的条数：{}".format(str(len(videolist))))
    driver.quit()
    if len(videolist) == 0:
        sys.exit(0)
    return videolist


def scrapy2IqyData(url):
    # 配置
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    href_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[*]/div[2]/a'
    title_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[*]/div[2]/a'
    sub_date_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[*]/div[3]/span[2]'

    hrefs = driver.find_elements_by_xpath(href_xpath)
    titles = driver.find_elements_by_xpath(title_xpath)
    sub_dates = driver.find_elements_by_xpath(sub_date_xpath)
    videolist = []
    index = 0
    for object in hrefs:
        href = hrefs[index].get_attribute('href')
        title = titles[index].text.replace("...","")
        sub_date = sub_dates[index].text.replace("上传","")
        print(sub_date + "   " + title + "   " + href)
        if sub_date == today:
            print(sub_date + "   " + title + "   " + href)
        videoDictionary = {"title": title, "href": href, "sub_date": sub_date}
        videolist.append(videoDictionary)
        index += 1
    driver.quit()
    return videolist

def getDataJob(all_videos,isMp4):
    # print("手机号 {} 在 {} 开始爬取  iqiyi视频地址".format(phone,datetime.datetime.now()))
    mkdir(video_path)
    #获取当天mysql里面已有的
    dbManager = DbManager()
    sql = "select * from iqy{} where  publish_status='1' AND publish_time like'{}%';".format(phone, today)
    res = dbManager.fetchall(sql)
    mysql_urls = []
    if res:
        for temp in res:
            mysql_urls.append(temp["video_web_url"])
    else:
        print("暂无数据")

    print("已入库的数据条数:{}".format(str(len(mysql_urls))))

    #超过当日最大发布量
    if len(mysql_urls) >=18:
        print("发布的条数已超过当日上线")
        sys.exit(0)

    #去除已存入数据库的
    not_use_videos=[]
    index=0
    for temp in all_videos:
        if temp["href"] in mysql_urls:
            index+=1
        else:
            not_use_videos.append(temp)
    no_use_count=len(not_use_videos)
    print("没入库的数据条数:{}".format(str(no_use_count)))

    count=0
    for i in not_use_videos:
        href = i["href"]
        title = i["title"]
        print(title)
        title = title.replace("...","")
        count+=1
        print("开始下载："+ str(count) + ":" + title + "  " + href)
        if isMp4:
            # 下载视频
            you_get = "you-get -o {} -O {} {} ".format(video_path, title, href)
            os.system(you_get)
        else:
            # 下载视频
            you_get = "you-get -o {} -O {}.mp4 {} ".format(video_path, title, href)
            os.system(you_get)

        #查看数据是否可用
        can_use_count = getCanUseVideo(href)
        if can_use_count >= 8:
            break

    #入库
    videos = getAllVideos(video_path)
    for video in videos:
        video_title = video.replace(".mp4", "")
        for i in not_use_videos:
            href = i["href"]
            title = i["title"]
            if video_title in title:
                dbManager = DbManager()
                sql = "INSERT INTO iqy{}(title,play_count,recommend_count,video_web_url,publish_time,publish_status,download_status) VALUES('{}',0,0,'{}','{}',0,1);".format(
                phone, video_title, href, today)
                res = dbManager.edit(sql)
                print(res)

if __name__ == '__main__':
    print("scrapyiqy程序已启动，开始获取 {} 所需的数据".format(phone))
    if phone=="13129972887":
        all_videos = scrapy_iqy(["https://list.iqiyi.com/www/22/1903-------------4-1-2-iqiyi-1-.html"])
        getDataJob(all_videos,False)
    elif phone=="13125005820":
        all_videos = scrapy_iqy(["https://list.iqiyi.com/www/22/1904-------------4-1-2-iqiyi-1-.html"])
        getDataJob(all_videos,False)
    elif phone=="15611729727":
        all_videos = scrapy_iqy(["https://list.iqiyi.com/www/22/1903-------------4-1-2-iqiyi-1-.html"])
        getDataJob(all_videos,False)
    elif phone=="15801303573":
        all_videos = scrapy_iqy(["https://list.iqiyi.com/www/3/74-------------4-1-2-iqiyi-1-.html","https://list.iqiyi.com/www/3/72-------------4-1-2-iqiyi-1-.html","https://list.iqiyi.com/www/3/70-------------4-1-2-iqiyi-1-.html"])
        getDataJob(all_videos,False)
    elif phone=="15110230192":
        all_videos = scrapy_iqy(["https://list.iqiyi.com/www/7/170-------------4-1-2-iqiyi-1-.html"])
        getDataJob(all_videos,False)
    elif phone=="18701233483":
        all_videos = scrapy_youku(["https://i.youku.com/i/UNTkxOTk1OTg5Ng==/videos","https://i.youku.com/i/UNTM5NzcxMDE2MA==/videos","https://i.youku.com/i/UNjUxNTU0OTU2OA==/videos","https://i.youku.com/i/UNjMyMjg4MjExMg==/videos"])
        getDataJob(all_videos,True)
    elif phone=="test":
        all_videos = scrapy2IqyData("https://www.iqiyi.com/u/1734792030/videos")
        getDataJob(all_videos)
