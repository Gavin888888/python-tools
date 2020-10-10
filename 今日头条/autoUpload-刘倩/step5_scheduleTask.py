# -*- coding: utf-8 -*-
import schedule
import time
import datetime
import shutil
import os

videos_path=os.path.abspath("13718665070")
video_upload_path=os.path.abspath("videos")
all_upload_py="python3 {}".format(os.path.abspath("allUpload2XG.py"))
videos=[]
day = 0
size = 10

def job1():
    print('Job1:每隔10秒执行一次的任务，每次执行2秒')
    print('Job1-startTime:%s' %(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    global day
    global size
    print(day)
    for filename in videos[day:day+size]:
        print(filename)
        shutil.copy('{}'.format(videos_path + "/" + filename), "{}/".format(video_upload_path) + filename)
    day+=size
    print(day)
    print(all_upload_py)
    os.system(all_upload_py)
    print('Job1-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job4():
    print('Job4:每天下午17:49执行一次，每次执行20秒')
    print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(20)
    print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

if __name__ == '__main__':
    videos = [f for f in os.listdir(videos_path)]
    # schedule.every(5).seconds.do(job1)
    schedule.every().day.at('07:34').do(job1)
    # schedule.every(30).seconds.do(job2)
    # schedule.every(1).minutes.do(job3)
    # schedule.every().day.at('12:11').do(job4)
    # schedule.every(5).to(10).seconds.do(job5)
    while True:
        schedule.run_pending()