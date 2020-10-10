import requests
import json
from iqiyi import *


def url2m3u8(data_url,file_name):
        url = "https://8090.ylybz.cn/jiexi2019/api.php"
        data = {"url": data_url,
                "ref": "0",
                "time": "1583762912",
                "other": "aHR0cHM6Ly93d3cuaXFpeWkuY29tL3ZfMTlyeDZsZTZ0ay5odG1sP3Zmcm09cGN3X3pvbmd5aQ=="}
        res = requests.post(url=url, data=data)
        resd = json.loads(res.text)
        print(resd)
        code = resd["code"]
        if code==200 :
                file_url = resd["url"]
                if file_url.find(".mp4")>=0:
                        print("ssssss")
                        dir_path=file_name
                        url = file_url
                        try:
                                res = requests.get(url, headers)
                        except requests.exceptions.MissingSchema:  # 捕获不完整URL的异常
                                target_url = target + '/' + url
                                res = requests.get(target_url, headers)
                        media_file_path = "./download_videos/" + dir_path + '.mp4'
                        if res.status_code != 200:
                                print('下载URL连接访问失败')

                        with open(media_file_path, 'ab')as f:
                                f.write(res.content)
                else:
                        main_other(file_name, file_url)
        else:
                stop=True
                re_request_time=0
                while stop:
                        url = "https://8090.ylybz.cn/jiexi2019/api.php"
                        data = {"url": data_url,
                                "ref": "0",
                                "time": "1583762912",
                                "other": "aHR0cHM6Ly93d3cuaXFpeWkuY29tL3ZfMTlyeDZsZTZ0ay5odG1sP3Zmcm09cGN3X3pvbmd5aQ=="}
                        res = requests.post(url=url, data=data)
                        resd = json.loads(res.text)
                        print(resd)
                        code = resd["code"]
                        if code == 200:
                                file_url = resd["url"]
                                main_other(file_name, file_url)
                                stop=False
                        else:
                                if re_request_time == 5:
                                        stop = False
                        re_request_time+=1
                        print("重试{}次".format(re_request_time))





url="https://pcw-api.iqiyi.com/video/video/recommend?area=zebra&cid=6&entity_source=&evid=&isInfinite=&page=1&play_platform=PC_QIYI&ppuid=&pru=&rec_id=13484882100&rltnum=10&size=10&type=video&uid=066839952672c7f21c470c1dbd8ef98d"
url="https://pcw-api.iqiyi.com/video/recommend/playguessulike?album_id=249627701&channel_id=6&device_id=066839952672c7f21c470c1dbd8ef98d&episode_id=12994680400&page=1&passport_id=&play_platform=PC_QIYI&ret_num=42&size=42&vip_type="

data={}
res = requests.post(url=url, data=data)
resd = json.loads(res.text)
print(resd)
mixinVideos=resd["data"]["list"]
for i in mixinVideos:
        url=i["playUrl"]
        name = i["name"]
        url2m3u8(url,name)



