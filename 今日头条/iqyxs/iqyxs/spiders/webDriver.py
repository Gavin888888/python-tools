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

import numpy as np
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont

toady = datetime.datetime.now().strftime('%Y-%m-%d')

#爱奇艺 视频url
iqy_urls = ["https://www.iqiyi.com/u/1801309092/videos","https://www.iqiyi.com/u/1630474990/videos"]

def scrapyData(url):
    #配置
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #启动浏览器
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    # sleep_time = 2
    # time.sleep(sleep_time)
    href_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[*]/div[1]/a'
    title_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[*]/div[2]/a'
    sub_date_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[*]/div[3]/span[2]'

    hrefs = driver.find_elements_by_xpath(href_xpath)
    titles = driver.find_elements_by_xpath(title_xpath)
    sub_dates = driver.find_elements_by_xpath(sub_date_xpath)

    videolist=[]
    index = 0
    for object in sub_dates:
        sub_date = object.text
        href = hrefs[index].get_attribute('href')
        title = titles[index].text
        # print(sub_date)
        # print(href)
        # print(title)
        sub_date=sub_date.replace("上传", "")
        # if sub_date==toady:
        videoDictionary = {"title": title.replace("...", ""), "href": href, "sub_date":sub_date }
        videolist.append(videoDictionary)
        index += 1
    driver.quit()
    return videolist
def mkdir(path):
   path = path.strip().rstrip('\\')
   is_exists = os.path.exists(path)
   if not is_exists:      # 校验目录是否存在
      os.makedirs(path)
      print('创建媒体目录')
   else:
      print('媒体目录已经存在')
   return path+'/'


def getDataJob():
    print('开始: %s 爬虫任务' % (toady))

    video_path="video_files"
    mkdir(video_path)

    global start_url
    for iqyurl in iqy_urls:
        videolist = scrapyData(iqyurl)
        count = 0
        for i in videolist:
            if count<15:
                href = i["href"]
                title = i["title"]
                print(str(count)+title + "  " + href)
                # 下载视频
                # you_get = "you-get -o {} -O {}.mp4 {}".format(video_path, title, href)
                # print(you_get)
                # os.system(you_get)
            else:
                break
            count+=1



def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, numpy.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)

if __name__ == '__main__':

    # schedule.every().day.at('00:00').do(getDataJob)
    # while True:
    #     schedule.run_pending()

    getDataJob()

    # step1: load in the video file

    # video = './video_files/1.mp4'
    # result_video = './video_files/1-1.mp4'
    #
    # sub = "ffmpeg -i " + video + " -i ./1.jpg -filter_complex overlay=W-w " + result_video + ''
    # videoresult = subprocess.run(args=sub, shell=True)


    # # 读取视频
    # cap = cv2.VideoCapture(video)
    # # 获取视频帧率
    # fps_video = cap.get(cv2.CAP_PROP_FPS)
    # # 设置写入视频的编码格式
    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # # 获取视频宽度
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # # 获取视频高度
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # videoWriter = cv2.VideoWriter(result_video, fourcc, fps_video, (frame_width, frame_height))
    # frame_id = 0
    # while (cap.isOpened()):
    #     ret, frame = cap.read()
    #     if ret == True:
    #         frame_id += 1
    #         left_x_up = int(frame_width / frame_id)
    #         left_y_up = int(frame_height / frame_id)
    #         right_x_down = int(left_x_up + frame_width / 10)
    #         right_y_down = int(left_y_up + frame_height / 10)
    #         # 文字坐标
    #         word_x = left_x_up + 5
    #         word_y = left_y_up + 25
    #         # cv2.rectangle(frame, (left_x_up, left_y_up), (right_x_down, right_y_down), (55, 255, 155), 5)
    #
    #         img = cv2ImgAddText(cv2.imread('img1.jpg'), "大家好，我是片天边的云彩", 10, 65, (0, 0, 139), 20)
    #
    #         cv2.putText(img)
    #
    #         # cv2.putText(frame, '岳云鹏这段经典之作又火了，全程包袱，这才是春晚..._%s' % frame_id, (word_x, word_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)
    #
    #
    #         videoWriter.write(frame)
    #     else:
    #         videoWriter.release()
    #         break



