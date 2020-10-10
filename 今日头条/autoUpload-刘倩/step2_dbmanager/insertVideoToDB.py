#!/usr/bin/env python
# coding:UTF-8
import logging
import sys
import os
import datetime
import shutil
from mysql import DbManager

phone="13125005820"
video_type="video_{}".format(phone)
videos_path= "./videos"
publish_videos_path="/Users/leili/Desktop/videos/video_{13125005820}".format(phone)

#创建表
def createTable():
    dbManager = DbManager()
    # # 读取 sql 文件文本内容
    # sql = open("{}".format(os.path.abspath("video.sql")), 'r', encoding='utf8')
    # sqltxt = sql.readlines()
    # # 读取之后关闭文件
    # sql.close()
    # # list 转 str
    # sql = "".join(sqltxt)

    sql = "CREATE TABLE `{}` (`id` bigint(32) NOT NULL AUTO_INCREMENT,`title` varchar(128) NULL,`des` varchar(255) NULL,`local_path` varchar(255) NULL,`play_count` int(255)  DEFAULT  0,`recommend_count` int(255)  DEFAULT  0,`publish_time` varchar(64) NULL,`release_time` varchar(64) NULL,`publish_status` int(255) DEFAULT  0,PRIMARY KEY (`id`) );".format(video_type)

    print(sql)
    # 连接数据库
    res = dbManager.connectDatabase()
    if not res:
            print(res)
    dbManager.cur.execute(sql)

if __name__ == '__main__':
    #print("mysql")
    #创建表
    createTable()
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
#----------------------------------
    # today_str = "2020-3-6"
    # today = datetime.datetime.strptime(today_str, "%Y-%m-%d")
    # offset=1
    #
    # files = [f for f in os.listdir(videos_path) if not f.startswith('.')]
    # dbManager = DbManager()
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


