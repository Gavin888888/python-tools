#!/usr/bin/env python
# coding:UTF-8

import scrapy
from sougou.items import SougouItem
import sys

class MySpider(scrapy.Spider):
    # 设置name
    name = "sougou"
    def start_requests(self):
        urls = []
        for i in range(1,100):
            print(i)
            new_url = "https://www.kugou.com/mvweb/html/index_9_%s.html" % (str(i))
            urls.append(new_url)
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    # 编写爬取方法
    def parse(self, response):
        print("-"*100)

        titles = response.xpath("/html/body/div[@class='frame']/div[@id='allcontent']/div[@class='rightCon']/div[@class='mvlist']/ul[@class='clearfix']/li[*]/span/text()").extract()
        webs = response.xpath("/html/body/div[@class='frame']/div[@id='allcontent']/div[@class='rightCon']/div[@class='mvlist']/ul[@class='clearfix']/li[*]/a/@href")
        tubimages = response.xpath("/html/body/div[@class='frame']/div[@id='allcontent']/div[@class='rightCon']/div[@class='mvlist']/ul[@class='clearfix']/li[*]/a/img/@_src").extract()
        item = SougouItem()
        print(tubimages)
        for idx, val in enumerate(webs):
            ahref=val.extract()
            id1 = ahref.replace("/mvweb/html/mv_", "")
            id = id1.replace(".html", "")
            print(id)
            weburl = "https://m3ws.kugou.com/mv/{}.html".format(id)
            print(weburl)
            title=titles[idx]
            print(title)
            thumb_url = tubimages[idx]
            print(thumb_url)
            item['id'] = id
            item['title'] = title
            item['web_url'] = weburl
            item['thumb_url'] =thumb_url
            yield item

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