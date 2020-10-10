# -*- coding:utf-8 -*-
import  os
import scrapy
from scrapy.selector import Selector
import json
import requests

class BlogSpider(scrapy.Spider):
    name = 'poem'

    def loadFont(jsonName):
        f = open(jsonName, encoding='utf-8')
        poemjson = json.load(f)
        return poemjson["RECORDS"]

    def start_requests(self):
        t = BlogSpider.loadFont('./poemtest.json')
        urls = []
        for i in range(1,len(t)):
            peom_data = t[i]
            url=peom_data["audio_html"]
            print(url)
            peom_id = peom_data["id"]
            yield scrapy.Request(url=url, callback=self.parse,meta={'id':peom_id})



    def parse(self, response):
        print("-"*100)
        itemid = response.meta['id']

        detail = response.xpath("/html/body/div/audio/@src").extract()

        url = detail[0]
        path = "audio/%s.mp3"%(itemid)
        r = requests.get(url)

        with open(path, "wb") as f:
            f.write(r.content)
        f.close()

