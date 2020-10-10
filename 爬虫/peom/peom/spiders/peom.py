# -*- coding:utf-8 -*-
import  os
import scrapy
from scrapy.selector import Selector
from peom.items import PeomItem
import json

class BlogSpider(scrapy.Spider):
    name = 'peom'

    def loadFont(jsonName):
        f = open(jsonName, encoding='utf-8')
        poemjson = json.load(f)
        return poemjson[0]["data"]

    def start_requests(self):
        t = BlogSpider.loadFont(os.path.abspath('peom/poem.json'))

        urls = []
        for i in range(1,len(t)):
            peom_data = t[i]
            mp3Url=peom_data["mp3Url"]
            if mp3Url == "null":
                print(" %s 没有音频" % (peom_data["id"]))
                new_url = "https://so.gushiwen.org/search.aspx?value=%s&peomid=%s" % (
                peom_data["first_sentence"], peom_data["id"])
                print(new_url)
                urls.append(new_url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        detail = response.xpath("/html/body/div[@class='main3']/div[@class='left']/div[@class='sons']/div[@class='tool']/div[@class='toolpinglun'][3]/a/img/@*").extract()
        print(response.url)
        peom_id = response.url.split('&peomid=', 1)

        temp_peom_id=detail[0]
        print("*" * 100)
        print(temp_peom_id)
        print("*" * 100)
        audio_id=temp_peom_id.replace("speakerimg", "")
        print("*" * 100)
        print(audio_id)
        print("*" * 100)
        peom_audio_hml= "https://so.gushiwen.org/viewplay.aspx?id=%s"%(audio_id)

        peom_item = PeomItem()
        peom_item['id'] = peom_id[1]
        peom_item['audio_html'] = peom_audio_hml
        yield peom_item

