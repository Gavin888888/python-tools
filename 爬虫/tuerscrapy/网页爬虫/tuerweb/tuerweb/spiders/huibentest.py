import scrapy
from scrapy.selector import Selector
from tuerweb.items import HuibenItem
import json
import demjson
import pymysql

class BlogSpider(scrapy.Spider):
    name = 'huibentest'
    def start_requests(self):
        urls = []
        types=[{"name":"qxglhb","count":4},{"name":"etcchb","count":14},{"name":"xgychb","count":12},{"name":"adjyhb","count":16}]
        print(types)
        for i in types:
            print(i["name"])
            print(i["count"])
            for j in range(1, i["count"]):
                if j==1:
                    new_url = "http://www.tuer123.com/huiben/%s/list-%s.html" % (i["name"], 0)
                    urls.append(new_url)
                else:
                    new_url = "http://www.tuer123.com/huiben/%s/list-%s.html" % (i["name"], j)
                    urls.append(new_url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            break


    def parse(self, response):
        detail = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box']/div[@class='g-main']/div[@class='m-lst j-lst']/div[@class='lst-paint']/a[@class='item'][*]/@href").extract()

        img_url = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box']/div[@class='g-main']/div[@class='m-lst j-lst']/div[@class='lst-paint']/a[@class='item'][*]/div[@class='cover-wp']/div[@class='u-cover']/img/@lz-src").extract()

        print("--"*100)
        print(detail)
        print(img_url)
        huiben_item = HuibenItem()
        for i in range(0, len(detail)):
            huiben_item['meta_url']="http:"+detail[i]
            huiben_item['id'] = huiben_item['meta_url'].split("/", 5)[5].replace(".html", "")
            huiben_item['img']=img_url[i]
            print(huiben_item)
            yield huiben_item


