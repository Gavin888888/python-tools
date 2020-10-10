# -*- coding: utf-8 -*-
import shutil
import  os
import scrapy
from scrapy.selector import Selector
import time
import json
import schedule
import time
import datetime
import shutil


json_path = "./video_json/1591869627.json"
video_path = "./download/"
allPageUrls = []
index=0

if not os.path.exists(video_path):
    os.mkdir(video_path)
else:
    print(video_path + '   is ok!')


def job4():
    print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    global index

    os.system("you-get -o {} {}".format(video_path, allPageUrls[index]))
    index+=1
    print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

if __name__ == "__main__":
    print(json_path + '   is ok!')
    f = open(json_path, encoding='utf-8')
    json = json.load(f)
    data=json["data"]
    keys=data.keys()

    for i in keys:
        title = data[i]["title"]
        pageUrl = data[i]["pageUrl"]
        downLoadPageUrl = "{}".format(pageUrl)
        print(title + "\n" + pageUrl + "\n" + downLoadPageUrl)
        allPageUrls.append(downLoadPageUrl)

    print(("*"*100))
    print(allPageUrls)
    schedule.every(2).minutes.do(job4)
    while True:
        schedule.run_pending()


