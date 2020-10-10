import requests
import os
from requests.packages import urllib3
import json
import time
current_time=int(time.time())

phones=["13125005820"]

def deleteVideo(phone):
    # phone = "13129972887"
    video_cookies = "{}/cookies/cookies_{}.json".format(os.path.abspath("."), phone)

    with open(video_cookies) as f:
        cookies = json.loads(f.read())
    cookiesDit = {}
    for cookie in cookies:
        # print(cookie)
        cookiesDit[cookie["name"]] = cookie["value"]

    # print(cookiesDit)
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win32; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/72.0.3626.109 Safari/537.36",
    }
    offset = 0
    for i in range(0, int(340 / 20)):

        url = 'https://mp.toutiao.com/xigua/api/video/getarticlesv2/?params={"SearchWord":"","Status":"all","Source":"all","Offset":%s,"Size":20,"StartTime":0,"EndTime":0,"Feature":1,"PageIdentyInstance":0}' % (
            str(offset))
        print(url)
        offset += 20
        urllib3.disable_warnings()
        req = requests.get(url, headers, cookies=cookiesDit, verify=False)
        json_object = json.loads(req.text)
        print(json_object)

        items = json_object["data"]["Items"]
        for i in items:
            # print(i)
            playCount = i["Data"]["PlayCount"]
            Title = i["Title"]
            Id = i["Id"]
            CreateTime = i["CreateTime"]
            ItemStatusCode = i["ArticleStatusInstance"]["ItemStatusCode"]

            # if ItemStatusCode != 20:
            #     print(str(playCount) + "\t" + Title+"\t")
            #     delete_url = 'https://mp.toutiao.com/xigua/api/video/articledelete/?params={"ItemId":"%s","SourceType":0,"DelSlaveId":"","Reason":""}' % (
            #         str(Id))
            #     urllib3.disable_warnings()
            #     req = requests.get(delete_url, headers, cookies=cookiesDit, verify=False)
            #     print(req)
            # and current_time - CreateTime >= 2 * 24 * 60 * 60
            if int(playCount) < 1000 :
                print(str(playCount) + "\t" + Title+"\t")
                delete_url = 'https://mp.toutiao.com/xigua/api/video/articledelete/?params={"ItemId":"%s","SourceType":0,"DelSlaveId":"","Reason":""}' % (
                    str(Id))
                urllib3.disable_warnings()
                req = requests.get(delete_url, headers, cookies=cookiesDit, verify=False)
                print(req.text)

for phone in phones:
    deleteVideo(phone)
