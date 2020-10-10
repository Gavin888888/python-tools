import pymysql

class SougouPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456789',
            'database': 'scrapy',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        sql = "INSERT INTO `sougoumv` (id,title,web_url,thumb_url) VALUES ('{}','{}','{}','{}');".format(item["id"],item["title"],item["web_url"],item["thumb_url"])
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()


    # # sql语句
    # insert_sql = """
    #            insert into huiben(meta_url,img,id) VALUES(%s,%s,%s)
    #            """
    # # 执行插入数据到数据库操作
    # self.cursor.execute(insert_sql, (item['meta_url'], item['img'], item['id']))
    # # 提交，不进行提交无法保存到数据库
    # self.conn.commit()


    #self.cursor.execute("UPDATE huiben SET type=%s,name=%s,url=%s,pics=%s,introduction=%s WHERE id=%s", (item['type'],item['name'],item['url'],item['pics'],item['introduction'],item['id']))

