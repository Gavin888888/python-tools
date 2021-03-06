#!/usr/bin/env python
# coding:UTF-8
import pymysql
import logging
import sys
import os
from pymysql.cursors import DictCursor

# 加入日志
# 获取logger实例
logger = logging.getLogger("dbSql")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(message)s')
# 文件日志
file_handler = logging.FileHandler("dbSql.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)

class DbManager:
    # 构造函数
    def __init__(self, host='127.0.0.1', port=3306, user='root',
                 passwd='123456789', db='xiguashipin', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.cur = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                        charset=self.charset)
        except:
            logger.error("connectDatabase failed")
            return False
        self.cur = self.conn.cursor(DictCursor)
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True


    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None, commit=False, ):
        # 连接数据库
        res = self.connectDatabase()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.execute(sql, params)
                # print(rowcount)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except:
            logger.error("execute failed: " + sql)
            logger.error("params: " + str(params))
            self.close()
            return False
        return rowcount

    # 查询所有数据
    def fetchall(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            logger.info("查询失败")
            return False
        self.close()
        results = self.cur.fetchall()
        # logger.info("查询成功" + str(results))
        return results

    # 查询一条数据
    def fetchone(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            logger.info("查询失败")
            return False
        self.close()
        result = self.cur.fetchone()
        logger.info("查询成功" + str(result))
        return result

    # 增删改数据
    def edit(self, sql, params=None):
        res = self.execute(sql, params, True)
        if not res:
            logger.info("操作失败")
            return False
        self.conn.commit()
        logger.info("操作成功" + str(res))
        return res

#创建表
def createTable(phone):
    dbManager = DbManager()
    sql = "CREATE TABLE `iqy{}` (`id` bigint(32) NOT NULL AUTO_INCREMENT,`title` varchar(128) NULL,`play_count` int(255)  DEFAULT  0,`recommend_count` int(255)  DEFAULT  0,`video_web_url` varchar(64) NULL,`publish_time` varchar(64) NULL,`publish_status` int(255) DEFAULT  0,`download_status` int(64) DEFAULT  0,UNIQUE (video_web_url),PRIMARY KEY (`id`) );".format(phone)
    print(sql)
    # 连接数据库
    res = dbManager.connectDatabase()
    if not res:
            print(res)
    dbManager.cur.execute(sql)
#创建表
def createTongjiTable():
    dbManager = DbManager()
    sql = "CREATE TABLE `iqytongji` (`id` bigint(32) NOT NULL AUTO_INCREMENT,`title` varchar(128) NULL,`videotype` varchar(128) NULL,`play_count` int(255)  DEFAULT  0,`recommend_count` int(255)  DEFAULT  0,PRIMARY KEY (`id`) );"
    print(sql)
    # 连接数据库
    res = dbManager.connectDatabase()
    if not res:
            print(res)
    dbManager.cur.execute(sql)


if __name__ == '__main__':
    print("mysql")
    # createTongjiTable()
    # ----------------------------------
    # 创建表
    # phones=["15611729727","13125005820","13129972887","15801303573","15110230192","18701233483"]
    # for phone in phones:
    #     createTable(phone)
    # ----------------------------------

    # ----------------------------------
    # dbManager = DbManager()
    # sql="select * from {} where publish_time='{}';".format("video_13718665070","2020-03-07")
    # update_sql = "select * from {} where publish_time='{}' and publish_status=0;".format("video_13718665070", "2020-03-07")
    # res=dbManager.fetchall(sql)
    # for tempVideo in res:
    #     print(tempVideo)
    #     sql_update = "UPDATE video_13718665070 SET publish_status = 0 WHERE id = '{}'".format(tempVideo["id"])
    #     print("更新状态sql={}".format(sql_update))
    #     dbManager.edit(sql_update)
# ----------------------------------
# today_str = "2020-3-6"
# today = datetime.datetime.strptime(today_str, "%Y-%m-%d")
# offset=1
#
# files = [f for f in os.listdir(videos_path) if not f.startswith('.')]

# for index, val in enumerate(files):
#     if index % 30 == 0:
#         day = today + datetime.timedelta(days=offset)
#         pushlist_date = str(day)[:10]
#         offset+=1
#     #视频名字
#     title=val
#     if len(title) < 5 :
#         title="   {}   ".format(title)
#     if len(title) > 34 :
#         video_type_list=title.split(".")
#         title="{}.{}".format(title[:30],video_type[1])
#     local_path="{}/{}".format(videos_path,val)
#     des_path = "{}/{}".format(publish_videos_path, title)
#     print(local_path)
#     print(des_path)
#     sql="INSERT INTO {}(title,des,local_path,play_count,recommend_count,publish_time,release_time,publish_status) VALUES('{}','','{}',0,0,'{}','',0);".format(video_type,title,des_path,pushlist_date)
#     print(sql)
#     res=dbManager.edit(sql)
#     if res==1:
#         shutil.copy(local_path,des_path)  # copy file
#         os.remove(local_path)