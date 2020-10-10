import scrapy
from scrapy.selector import Selector
from tuerweb.items import TuerwebItem
import json


class BlogSpider(scrapy.Spider):
    name = 'tuerweb'

    def start_requests(self):
        urls = []
        for i in range(1,21):
            new_url = "http://m.tuer123.com/zt/list-%s.html" % (i)
            urls.append(new_url)
        print(urls)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        rs = json.loads(response.text)

        data = rs['result']['data']

        gushi_item = TuerwebItem()
        for temp in data:
            gushi_item['id'] = temp["id"]
            gushi_item['name'] = temp["name"]
            gushi_item['type'] = temp["type"]
            gushi_item['pinyin'] = temp["pinyin"]
            gushi_item['pc_instruction'] = temp["pc_instruction"]
            gushi_item['gif'] = temp["gif"]
            gushi_item['pic'] = temp["pic"]
            yield gushi_item


        # detail = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box'][2]/div[@class='m-lst j-lst']/div[@class='lst-sbj']/a[@class='item']/@href").extract()
        # img_url = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box'][2]/div[@class='m-lst j-lst']/div[@class='lst-sbj']/a[@class='item'][*]/div[@class='u-cover']/img/@lz-src").extract()
        # name = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box'][2]/div[@class='m-lst j-lst']/div[@class='lst-sbj']/a[@class='item'][*]/div[@class='u-cover']/img/@alt").extract()
        # print('\033[1;31;20m')  # 下一目标输出背景为黑色，颜色红色高亮显示  /div[@class='u-cover']/img/@lz-src .extract()
        # print('*' * 100)
        # print(detail)
        # print('*' * 100)
        # print(img_url)
        # print('*' * 100)
        # print(name)
        # print('*' * 100)
        # print('\033[0m')

        # gushi_item = TuerwebItem()
        #
        # for i in range(0, len(detail)):
        #     print(i)
        #     print(detail[i],img_url[i],name[i])
        #     gushi_item['name'] = name[i]
        #     gushi_item['instruction'] = detail[i]
        #     gushi_item['pic'] = img_url[i]
        #     gushi_item['time'] = ""
        #     gushi_item['audio_url'] = ""
        #     gushi_item['audio_loc'] = ""
        #     yield gushi_item

