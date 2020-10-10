# -*- coding: utf-8 -*-
import scrapy
import json
from Goodboy.items import audioItem
from Goodboy.items import specialList

class SpiderCsdnSpider(scrapy.Spider):
    name = 'spider_tuergushi'
    # allowed_domains = ['csdn.net']
    # start_urls = ['https://appapply.img4399.com/rr/api.tuer123.com/app/iphone/v1.5/index/index.html?age=1&startKey=']
    start_urls = ['http://api.tuer123.com/app/iphone/v1.5/index/index.html?age=1&startKey=']
    url = start_urls[0]
    pageNum = 1
    specialList_count = 0
    audioItem_count = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,headers={
                'X-Api-Appid': "8GSWdsDnPSqUkXQc",
                'X-Api-Time': "1566374573",
                'X-Tuer-Proxy': "0",
                'X-Api-Nonce': "118D41D2-AB80-4305-B10B-6BE5A721ACE0",
                'mdeviceId': "50F778A6-FDF3-400F-9523-40444ED088D2",
                'X-Api-Sign': "ffcbb755c743a6154996863f9f2f0cfa",
                'X-Tuer-From': "TYvhEqGPI1FZbNB+i/jP/Q==",
                'User-Agent': "BunnyEarsStory/1.9.0(ios;iPhone8,1;ios 12.2.0;375.0x667.0;WIFI;appstore;100;CTRadioAccessTechnologyLTE,4G,460,02,cn,true;)"
            })

    def parse(self, response):
        rs = json.loads(response.text)

        specialList_response = rs['result']['specialList']['data']

        item = specialList()
        audio_item = audioItem()
        for quote in specialList_response:
            self.specialList_count+=1
            item['id'] = quote["id"]
            item['name'] = quote["name"]
            item['free_num'] = quote["free_num"]
            item['type'] = quote["type"]
            item['dateline'] = quote["dateline"]
            item['pic'] = quote["pic"]
            item['gif'] = quote["gif"]
            item['subtitle'] = quote["subtitle"]
            item['play_num'] = quote["play_num"]
            item['source_num'] = quote["source_num"]
            item['charge'] = quote["charge"]
            item['playNum'] = quote["playNum"]
            item['formatPlayNum'] = quote["formatPlayNum"]
            yield item
            list = quote["list"]
            for audio in list:
                self.audioItem_count += 1
                audio_item['fatherid'] = str(quote["id"])
                audio_item['id'] = audio["id"]
                audio_item['storyType'] = audio["storyType"]
                audio_item['pic'] = audio["pic"]
                audio_item['name'] = audio["name"]
                audio_item['time'] = audio["time"]
                audio_item['url'] = audio["url"]
                audio_item['md5'] = audio["md5"]
                audio_item['play_num'] = audio["play_num"]
                audio_item['uploader'] = audio["uploader"]
                audio_item['playNum'] = audio["playNum"]
                audio_item['formatPlayNum'] = audio["formatPlayNum"]
                yield audio_item


        # 多url， 请求的手动发送
        total = rs['result']['total']
        pageSize = rs['result']['pageSize']
        print('\033[1;31;40m')  # 下一目标输出背景为黑色，颜色红色高亮显示
        print('*' * 50)
        print(total)
        print(pageSize)
        print('*' * 50)
        print('\033[0m')
        if self.pageNum <= total/pageSize + 1:  # 控制！否则无限递归了。。
            self.pageNum += 1
            print('爬第：%d 页' % self.pageNum)
            new_url = "%s%s" % (self.url, self.pageNum)
            print(new_url)
            # callback 回调函数，页面进行解析
            yield scrapy.Request(url=new_url,headers={
                'X-Api-Appid': "8GSWdsDnPSqUkXQc",
                'X-Api-Time': "1566374573",
                'X-Tuer-Proxy': "0",
                'X-Api-Nonce': "118D41D2-AB80-4305-B10B-6BE5A721ACE0",
                'mdeviceId': "50F778A6-FDF3-400F-9523-40444ED088D2",
                'X-Api-Sign': "ffcbb755c743a6154996863f9f2f0cfa",
                'X-Tuer-From': "TYvhEqGPI1FZbNB+i/jP/Q==",
                'User-Agent': "BunnyEarsStory/1.9.0(ios;iPhone8,1;ios 12.2.0;375.0x667.0;WIFI;appstore;100;CTRadioAccessTechnologyLTE,4G,460,02,cn,true;)"
            },callback=self.parse)
        else:
            print('\033[1;31;40m')  # 下一目标输出背景为黑色，颜色红色高亮显示
            print('*' * 100)
            print(self.specialList_count)
            print(self.audioItem_count)
            print('*' * 100)
            print('\033[0m')
