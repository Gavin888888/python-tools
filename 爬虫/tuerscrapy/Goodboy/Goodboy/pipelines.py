import pymysql

class MysqlPipeline(object):
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
        # print(item)
        # print( item.keys())
        if "gif" in item.keys():
            #分类数据
            print("存在")
            # sql语句
            insert_sql = """
                   insert into specialList(id,name,free_num,type,dateline,pic,gif,subtitle,play_num,source_num,charge,playNum,formatPlayNum) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   """
            # 执行插入数据到数据库操作
            self.cursor.execute(insert_sql, (item['id'], item['name'], item['free_num'], item['type'],
                                             item['dateline'], item['pic'], item['gif'], item['subtitle'],
                                             item['play_num'],
                                             item['source_num'], item['charge'],
                                             item['playNum'], item['formatPlayNum']))
        else:
            print("不存在")
            # sql语句
            insert_sql = """
                    insert into audioItem(fatherid,id,storyType,pic,name,time,url,md5,play_num,uploader,playNum,formatPlayNum) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                             """
            # 执行插入数据到数据库操作
            self.cursor.execute(insert_sql, (item['fatherid'],item['id'], item['storyType'], item['pic'], item['name'],
                                             item['time'], item['url'], item['md5'], item['play_num'],
                                             item['uploader'],
                                             item["playNum"], item['formatPlayNum']))

        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
