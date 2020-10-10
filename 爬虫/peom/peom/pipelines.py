import pymysql

class PeomPipeline(object):
    """
    同步操作
    """

    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'goodboy',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        # print("--------pipeline---------")
        # sql语句
        insert_sql = """
                   insert into poemtest(id,audio_html) VALUES(%s,%s)
                   """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['id'],  item['audio_html']))


        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
