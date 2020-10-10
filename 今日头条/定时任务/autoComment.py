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


phones=["15611729727","13125005820","15801303573","15110230192","13129972887","18701233483"]

phone="18701233483"
video_cookies = "{}/cookies/cookies_{}.json".format(os.path.abspath("."), phone)

with open(video_cookies) as f:
    cookies = json.loads(f.read())
cookiesDit = {}
for cookie in cookies:
    cookiesDit[cookie["name"]] = cookie["value"]

def  commentVideo(video_id):
    phone = "15611729727"
    video_cookies = "{}/cookies/cookies_{}.json".format(os.path.abspath("."), phone)
    with open(video_cookies) as f:
        cookies = json.loads(f.read())
    cookiesDit = {}
    for cookie in cookies:
        cookiesDit[cookie["name"]] = cookie["value"]

    comments_url="https://www.ixigua.com/tlb/comment/article/v5/tab_comments/?tab_index=0&count=20&offset=10&group_id=6804403810778219020&item_id=6804403810778219020&aid=1768"
    urllib3.disable_warnings()
    req1 = requests.get(comments_url, cookies=cookiesDit, verify=False)
    commentss = json.loads(req1.text)
    comments=commentss["data"]
    for i in comments:
        comment=i["comment"]["text"]
        print(comment)
        video_id="6797592654499545612"
        url = 'https://www.ixigua.com/tlb/comment/2/data/v5/post_message/?aid=1768'
        data = {'group_id': video_id, 'item_id': video_id, "text": comment, "aid": "1768", "image_info": []}

        urllib3.disable_warnings()
        req = requests.get(url, data, cookies=cookiesDit, verify=False)
        json_object = json.loads(req.text)
        print(json_object)



url = 'https://mp.toutiao.com/xigua/api/video/getarticlesv2/?params={"SearchWord":"","Status":"all","Source":"all","Offset":0,"Size":20,"StartTime":0,"EndTime":0,"Feature":1,"PageIdentyInstance":0}'
urllib3.disable_warnings()
req = requests.get(url, cookies=cookiesDit, verify=False)
json_object = json.loads(req.text)
print(json_object)
Items=json_object["data"]["Items"]
for i in Items:
    print(i)
    commentVideo(i["IdStr"])
    break

