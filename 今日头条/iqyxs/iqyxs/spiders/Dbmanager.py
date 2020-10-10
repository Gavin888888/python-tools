#!/usr/bin/env python
# coding:UTF-8
import pymysql
import logging
import sys
import os
from pymysql.cursors import DictCursor


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
    def __init__(self, host='localhost', port=3306, user='root',
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
        logger.info("查询成功" + str(results))
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
        self.close()
        logger.info("操作成功" + str(res))
        return res


#创建表
def createTable(sql):
    dbManager = DbManager()
    print(sql)
    # 连接数据库
    res = dbManager.connectDatabase()
    if not res:
            print(res)
    dbManager.cur.execute(sql)

if __name__ == '__main__':
    print("mysql")
    sql = "CREATE TABLE `video_13125005820` (`id` bigint(32) NOT NULL AUTO_INCREMENT,`title` varchar(128) NULL,`des` varchar(255) NULL,`local_path` varchar(255) NULL,`play_count` int(255)  DEFAULT  0,`recommend_count` int(255)  DEFAULT  0,`publish_time` varchar(64) NULL,`release_time` varchar(64) NULL,`publish_status` int(255) DEFAULT  0,PRIMARY KEY (`id`) );"
    createTable(sql)
    # # 读取 sql 文件文本内容
    # sql = open("{}".format(os.path.abspath("video.sql")), 'r', encoding='utf8')
    # sqltxt = sql.readlines()
    # # 读取之后关闭文件
    # sql.close()
    # # list 转 str
    # sql = "".join(sqltxt)
    # print(sql)
    # # 连接数据库
    # res = dbManager.connectDatabase()
    # if not res:
    #         print(res)
    # dbManager.cur.execute(sql)