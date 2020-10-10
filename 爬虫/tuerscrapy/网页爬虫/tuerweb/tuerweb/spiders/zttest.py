import scrapy
from scrapy.selector import Selector
from tuerweb.items import ZtItem
import json
import demjson
import pymysql

class BlogSpider(scrapy.Spider):
    name = 'zttest'
    def start_requests(self):
        urls = []
        for i in range(1, 20):
            new_url = "http://m.tuer123.com/zt/list-%s.html" % (i)
            urls.append(new_url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        response_object=json.loads(response.text)
        data=response_object["result"]["data"]
        zt_item = ZtItem()
        for i in range(0, len(data)):
            temp=data[i]
            zt_item['id']=temp["id"]
            zt_item['title'] = temp["name"]
            zt_item['type'] = temp["type"]
            zt_item['instruction'] = temp["pc_instruction"]
            zt_item['gif'] = temp["gif"]
            zt_item['pic'] = temp["pic"]
            zt_item['meta_url'] = "http://www.tuer123.com/zt/%s/"%(temp["pinyin"])
            yield zt_item


