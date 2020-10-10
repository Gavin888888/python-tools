# -*- coding: utf-8 -*-
import scrapy
import json


class SpiderCsdnSpider(scrapy.Spider):
    name = 'iqyxsss'
    start_urls = ['https://mp.toutiao.com/xigua/api/video/getarticlesv2/?params={"SearchWord":"","Status":"all","Source":"all","Offset":20,"Size":20,"StartTime":0,"EndTime":0,"Feature":1,"PageIdentyInstance":0}']
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        print(response.text)

