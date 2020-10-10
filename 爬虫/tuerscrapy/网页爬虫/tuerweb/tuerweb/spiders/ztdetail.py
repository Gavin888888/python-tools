import scrapy
from scrapy.selector import Selector
from tuerweb.items import ZtItem
import json
import demjson
import pymysql
import os
import urllib.request

class BlogSpider(scrapy.Spider):
    name = 'ztdetail'
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
                      select * from zt where gif like '%gif'
                      """
        # 执行插入数据到数据库操作
        cursor.execute(query_sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        respone=[]
        for row in rows:
            print(row[0])
            print(row[9])
            respone.append({"id":row[0],"gif":row[9]})
        return respone

    def saveImgToLocal(self,file_path,file_name,image_url):
        try:
            print(file_path)
            print(file_name)
            print(image_url)
            if not os.path.exists(file_path):
                os.makedirs(file_path)  # 如果没有这个path则直接创建
            filename = '{}/{}.gif'.format(file_path, file_name)
            print(filename)
            urllib.request.urlretrieve(image_url, filename=filename)
            print(11111)
        except IOError as e:
            print(1, e)
        except Exception as e:
            print(2, e)

    def start_requests(self):
        data=self.loadData();
        urls = data
        for url in urls:
            print('*' * 100)
            print(url)
            self.saveImgToLocal(os.path.abspath('ztimg'),url["id"],url["gif"])

    def parse(self, response):
        print(response)
        # title = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box']/div[@class='m-sbj m-sbj-audio lst-audio']/div[@class='m-lst j-lst']/div[@class='item'][*]/a[@class='u-tt']/text()").extract()
        # detail_url = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box']/div[@class='m-sbj m-sbj-audio lst-audio']/div[@class='m-lst j-lst']/div[@class='item'][*]/a[@class='u-tt']/@href").extract()
        # print('\033[1;31;20m')  # 下一目标输出背景为黑色，颜色红色高亮显示  /div[@class='u-cover']/img/@lz-src .extract()
        # print('*' * 100)
        # print(title[0])
        # print(detail_url[0])

        # url=js_obj["url"]
        # name = js_obj["name"]
        # pics = js_obj["pics"]
        # huiben_item = HuibenItem()
        # huiben_item['id']=response.url.split("/", 5)[5].replace(".html", "")
        # huiben_item['type']=response.url.split("/", 5)[4]
        # huiben_item['name']=name
        # huiben_item['url']=url
        # huiben_item['pics']=pics
        # huiben_item['introduction']=introduct[0]
        # yield huiben_item
        print('*' * 100)
        print('\033[0m')


