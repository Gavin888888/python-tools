#!/usr/bin/env python
# coding:UTF-8
import scrapy
import sys
import requests
import json

class MySpider(scrapy.Spider):
    # 设置name
    name = "iqiyi"
    def start_requests(self):
        urls = []
        # url = "https://www.iqiyi.com/v_19rx502zb8.html"
        url="https://pcw-api.iqiyi.com/video/video/recommend?area=zebra&cid=6&entity_source=&evid=&isInfinite=&page=1&play_platform=PC_QIYI&ppuid=&pru=&rec_id=13605749800&rltnum=10&size=10&type=video&uid=e3a3afccfe9833202dee25393d4df0dd"
        yield scrapy.Request(url=url, callback=self.parse)

    # 编写爬取方法
    def parse(self, response):
        print("-"*100)
        print(response.data)
        res=json.loads(response.text)
        print(res.data)

        print("+" * 100)

            # yield huiben_item

        # for line in response.xpath('//li[@class=" j_thread_list clearfix"]'):
        #     # 初始化item对象保存爬取的信息
        #     item = DetailItem()
        #     # 这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        #     item['title'] = line.xpath(
        #         './/div[contains(@class,"threadlist_title pull_left j_th_tit ")]/a/text()').extract()
        #     item['author'] = line.xpath(
        #         './/div[contains(@class,"threadlist_author pull_right")]//span[contains(@class,"frs-author-name-wrap")]/a/text()').extract()
        #     item['reply'] = line.xpath(
        #         './/div[contains(@class,"col2_left j_threadlist_li_left")]/span/text()').extract()
        #     yield item