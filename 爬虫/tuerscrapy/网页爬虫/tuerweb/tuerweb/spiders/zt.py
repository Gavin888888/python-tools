import scrapy
from scrapy.selector import Selector
from tuerweb.items import ZtItem
import json
import demjson
import pymysql

class BlogSpider(scrapy.Spider):
    name = 'zt'
    def loadData(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'goodboy',
            'charset': 'utf8'
        }
        conn = pymysql.connect(**dbparams)
        cursor = conn.cursor()
        query_sql = """
                      select meta_url from zt
                      """
        # 执行插入数据到数据库操作
        cursor.execute(query_sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        respone=[]
        for row in rows:
            respone.append(row[0])
        return respone

    def start_requests(self):
        data=self.loadData();
        urls = data
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        gushi_detail_url = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box']/div[@class='m-sbj m-sbj-audio lst-audio']/div[@class='m-lst j-lst']/div[@class='item'][*]/a[@class='u-tt']/@href").extract()
        huiben_detail_url = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box']/div[@class='m-sbj m-sbj-pt lst-paint']/div[@class='m-lst j-lst']/a/@href").extract()

        print('\033[1;31;20m')  # 下一目标输出背景为黑色，颜色红色高亮显示  /div[@class='u-cover']/img/@lz-src .extract()
        print('*' * 100)

        print(gushi_detail_url)
        print(huiben_detail_url)
        sub_id=""
        if len(gushi_detail_url)>0:
            sub_id_array = []
            for url in gushi_detail_url:
                temp_id = url.split("/", 6)[5].replace(".html", "")
                sub_id_array.append(temp_id)
                print(sub_id_array)
            sub_id_array.sort()
            sub_id = ','.join(sub_id_array)
        elif len(huiben_detail_url)>0:
            sub_id_array = []
            for url in huiben_detail_url:
                temp_id = url.split("/", 6)[5].replace(".html", "")
                sub_id_array.append(temp_id)
                print(sub_id_array)
            sub_id_array.sort()
            sub_id = ','.join(sub_id_array)
        zt_item = ZtItem()
        zt_item['value']=sub_id
        zt_item['meta_url'] = response.url
        print(zt_item)
        yield zt_item

        print('*' * 100)
        print('\033[0m')


