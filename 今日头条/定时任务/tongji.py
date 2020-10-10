import requests
import os
from requests.packages import urllib3
import json
import time
from mysql import DbManager
dbManager = DbManager()
import time, datetime

import matplotlib.font_manager as fm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import csv

chinesefont = fm.FontProperties(fname='/Users/leili/Documents/aspire_work/zhty-service/sport-api-parent/sport-timer-task/src/main/resources/htmlUrl/public/font/MSYH.TTC')

current_time=int(time.time())

phones=["15611729727","13125005820","15801303573","15110230192","13129972887","18701233483"]
# phones=["18701233483"]
def getVideo(phone):
    video_cookies = "{}/cookies/cookies_{}.json".format(os.path.abspath("."), phone)

    with open(video_cookies) as f:
        cookies = json.loads(f.read())
    cookiesDit = {}
    for cookie in cookies:
        cookiesDit[cookie["name"]] = cookie["value"]

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/72.0.3626.109 Safari/537.36",
    }
    offset = 0
    for i in range(0, int(2000 / 20)):
        url = 'https://mp.toutiao.com/xigua/api/video/getarticlesv2/?params={"SearchWord":"","Status":"all","Source":"all","Offset":%s,"Size":20,"StartTime":0,"EndTime":0,"Feature":1,"PageIdentyInstance":0}' % (
            str(offset))
        offset += 20
        urllib3.disable_warnings()
        req = requests.get(url, headers, cookies=cookiesDit, verify=False)
        json_object = json.loads(req.text)
        items = json_object["data"]["Items"]
        if len(items)==0:
            break
        for i in items:
            playCount = i["Data"]["PlayCount"]
            RecommendCount = i["Data"]["RecommendCount"]
            Title = i["Title"]
            CreateTime = i["CreateTime"]
            print(Title+"\t"+str(playCount)+"\t"+str(RecommendCount)+"\t"+str(CreateTime)+"\t")
            if current_time - CreateTime >= 5 * 24 * 60 * 60:
                sql = "INSERT INTO iqytongji(title,videotype,play_count,recommend_count,publish_time) VALUES('{}','{}','{}','{}','{}');".format(
                    Title, phone, playCount, RecommendCount,str(CreateTime))
                print(sql)
                res = dbManager.edit(sql)

if __name__ == '__main__':
    print("统计程序")
    #统计数据入库
    # for phone in phones:
    #     getVideo(phone)

    dbManager = DbManager()
    sql_update = "SELECT * FROM iqytongji;"
    res = dbManager.fetchall(sql_update)
    rows=[]
    for i in res:
        play_count=i["play_count"]
        recommend_count = i["recommend_count"]

        if recommend_count < 100000:
            continue
        timeStamp = int(i["publish_time"])
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("2020-03-24 %H:%M:%S", timeArray)

        row = [recommend_count,otherStyleTime]

        rows.append(row)

    print(rows)
    headers = ['playcount','dtime' ]
    with open('test.csv', 'w')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    df = pd.read_csv('/Users/leili/Desktop/定时任务/test.csv', parse_dates=['dtime'])
    print(df)
    plt.plot_date(df.dtime, df.playcount, fmt='b.')

    ax = plt.gca()
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))  # 设置时间显示格式
    ax.xaxis.set_major_locator(AutoDateLocator(maxticks=24*2))  # 设置时间间隔

    plt.xticks(rotation=90, ha='center')
    # label = ['speedpoint']
    # plt.legend(label, loc='upper right')

    plt.grid(ls='--')

    ax.set_title(u'推荐量', fontproperties=chinesefont, fontsize=14)
    ax.set_xlabel('time')
    ax.set_ylabel('count')

    plt.show()
