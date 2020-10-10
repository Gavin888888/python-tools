import scrapy
from scrapy.selector import Selector
from tuerweb.items import HuibenItem
import json
import demjson
import pymysql

class BlogSpider(scrapy.Spider):
    name = 'huiben'
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
                      select meta_url from huiben
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
        introduct = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box g-box-main']/div[@class='m-info j-toggleCt']/p[@class='u-cxt j-toggleCtx']/text()").extract()

        js = response.xpath("/html/body/script").extract()

        print('\033[1;31;20m')  # 下一目标输出背景为黑色，颜色红色高亮显示  /div[@class='u-cover']/img/@lz-src .extract()
        print('*' * 100)
        script=js[3].split("config.data =",2)
        script1=script[1].replace("; </script>","")
        js_obj = demjson.decode(script1)
        url=js_obj["url"]
        name = js_obj["name"]
        pics = js_obj["pics"]
        huiben_item = HuibenItem()
        huiben_item['id']=response.url.split("/", 5)[5].replace(".html", "")
        huiben_item['type']=response.url.split("/", 5)[4]
        huiben_item['name']=name
        huiben_item['url']=url
        huiben_item['pics']=pics
        huiben_item['introduction']=introduct[0]
        yield huiben_item
        print('*' * 100)
        print('\033[0m')


