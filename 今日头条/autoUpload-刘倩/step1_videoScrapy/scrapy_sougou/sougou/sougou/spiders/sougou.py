import scrapy
from step1_videoScrapy.scrapy_sougou.sougou.sougou.items import SougouItem
import sys

class MySpider(scrapy.Spider):
    # 设置name
    name = "sougou"
    def start_requests(self):
        urls = []
        for i in range(1,2):
            print(i)
            new_url = "https://www.kugou.com/mvweb/html/index_13_%s.html" % (str(i))
            urls.append(new_url)
            print(new_url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            break
    # 编写爬取方法
    def parse(self, response):
        print("-"*100)

        titles = response.xpath("/html/body/div[@class='frame']/div[@id='allcontent']/div[@class='rightCon']/div[@class='mvlist']/ul[@class='clearfix']/li[*]/span/text()").extract()
        tubimages = response.xpath("/html/body/div[@class='frame']/div[@id='allcontent']/div[@class='rightCon']/div[@class='mvlist']/ul[@class='clearfix']/li[*]/a/@href")

        for l in tubimages:
            print(l.extract())
        print("+" * 100)
        item = SougouItem()
        # for i in range(0, len(detail)):
        #     huiben_item['meta_url'] = "http:" + detail[i]
        #     huiben_item['id'] = huiben_item['meta_url'].split("/", 5)[5].replace(".html", "")
        #     huiben_item['img'] = img_url[i]
        #     print(huiben_item)
        #     yield huiben_item

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