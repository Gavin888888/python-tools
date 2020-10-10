import scrapy
from scrapy.selector import Selector
from tuerweb.items import GushiItem
import json
import demjson
import pymysql

class BlogSpider(scrapy.Spider):
    name = 'gushi'
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
                      select url from gushiweb
                      """
        # 执行插入数据到数据库操作
        cursor.execute(query_sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        respone=[]
        for row in rows:
            print(row[0])
            respone.append(row[0])
        return respone

    def start_requests(self):
        data=self.loadData();
        print(data)
        urls = data
        # types=[{"name":"tegs","count":15},{"name":"thgs","count":15},{"name":"sqgs","count":50},{"name":"yygs","count":15},{"name":"cygs","count":27},{"name":"shgs","count":8},{"name":"ywgs","count":9}]
        # print(types)
        # for i in types:
        #     print(i["name"])
        #     print(i["count"])
        #     for j in range(2, i["count"]):
        #         new_url = "http://m.tuer123.com/gushi/%s/list-%s.html" %(i["name"],j)
        #         urls.append(new_url)
        #         break

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        img = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box'][1]/div[@class='m-audio']/div[@class='audio-main']/div[@class='u-cover']/img/@lz-src").extract()
        title = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box'][1]/div[@class='m-audio']/div[@class='audio-main']/h1[@class='u-tt']/text()").extract()
        introduct = response.xpath("/html/body/div[@class='container']/div[@class='g-cc']/div[@class='g-wp']/div[@class='g-wpc']/div[@class='g-mn']/div[@class='g-mnc']/div[@class='g-box'][1]/div[@class='m-audio']/div[@class='audio-detail']/div[@class='m-tab-ct j-tab-ct']/div[@class='m-desc j-toggleCt j-toggleCt-1']/div[@class='u-desc']/p[@class='u-detail j-toggleCtx']/text()").extract()
        js = response.xpath("/html/body/script").extract()
        print('\033[1;31;20m')  # 下一目标输出背景为黑色，颜色红色高亮显示  /div[@class='u-cover']/img/@lz-src .extract()
        print('*' * 100)
        script=js[3].split("config.data =",2)
        script1=script[1].replace("; </script>","")
        script2=script1.replace(" { ","")
        script3 = script2.replace("  }", "")
        all=script3.split(",",(3))
        url=all[0].replace("url:'","").replace("'","")
        time = all[1].replace(" time:'", "").replace("'", "")
        id = all[2].replace(" id:'", "").replace("'", "")
        print(url)
        print(time)
        print(id)
        print(img)
        print(title[0])
        print(introduct[0])
        gushi_item = GushiItem()
        gushi_item['id'] = id
        gushi_item['name'] = title[0]
        gushi_item['url'] = url
        gushi_item['pic'] = img[0]
        gushi_item['time'] = time
        gushi_item['introduction'] = introduct[0]
        gushi_item['type'] = response.url.split("/", 5)[4]
        gushi_item['gif'] = ""
        gushi_item['play_num'] = ""
        gushi_item['md5'] = ""
        yield gushi_item

        print('*' * 100)
        print('\033[0m')

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

