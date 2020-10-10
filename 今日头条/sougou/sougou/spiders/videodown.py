#!/usr/bin/env python
# coding:UTF-8
import pymysql
import datetime
import scrapy
from sougou.items import SougouItem
import sys
from pymysql.cursors import DictCursor
from selenium import webdriver
import time
import requests
import re
import hashlib
import json
import os
from requests.adapters import HTTPAdapter


def create_folder(name):  # 创建文件夹
    try:
        print(name )
        if '{}'.format(name) not in os.listdir():  # 如果不存在
            os.makedirs('{}'.format(name))  # 则创建
    except:
        return ''

def clean_txt(title):  # 清洗标题中不能用于命名文件的字符
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    title = re.sub(rstr, "_", title)  # 替换为下划线
    return title

headers = {'referer': 'https://www.kugou.com/song/', 'User-Agent': 'Mozilla/5.0'}
def get_one_page(url, headers=headers, code='utf-8'):  # 访问一个页面 返回页面信息
    try:
        s = requests.Session()  # 保持会话
        s.mount('http://', HTTPAdapter(max_retries=3))  # 最大重试
        s.mount('https://', HTTPAdapter(max_retries=3))
        r = s.get(url, headers=headers, timeout=15)  # 超时设置
        r.raise_for_status()  # 状态码 如果不是200则报错
        r.encoding = code  # r.apparent_encoding#字符类型
        return r.text  # 返回页面
    except Exception as e:
        t = time.strftime('%Y/%m/%d %H:%M:%S %a')  # 时间格式化
        with open(r'./kugou/Exception.txt', 'a+', encoding='utf-8') as f:
            f.write('time:{}\n\nurl:{}\n\n{}\n\n'.format(t, url, e))


def get_song_mv(keyword):  # 传入搜索关键词 返回MV 哈希值列表
    url = "http://mvsearch.kugou.com/mv_search?&keyword={}&pagesize=50&page=1".format(keyword)  # mv搜索接口
    # print('正在访问Mv搜索页面：{}'.format(url))
    res = get_one_page(url, headers={'User-Agent': 'Mozilla/5.0'})  # 调用get one page函数
    msgs = re.findall(r'{("MixSongID".*?)}', res, re.S)  # 所有mv
    LL = []
    for i in range(len(msgs)):
        MvName = clean_txt(re.findall(r'"FileName":"(.*?)"', msgs[i], re.S)[0])  # 单个Mv名字
        print('{}>>> {}'.format(str(i + 1), MvName))
        MvHash = re.findall(r'"MvHash":"(.*?)"', msgs[i], re.S)[0]  # 单个哈希值
        LL.append([MvName, MvHash])  # 所有 名字 哈希值形成列表
    number = input("\n请输入要下载的歌曲序号,以英文','号分隔,如:1,3 --（输入-1退出程序）(回车下载全部): ")
    if number == '':
        ll = LL
        return ll  # 等于空返回列表所有
    elif number == '-1':
        exit()# 等于-1返回空列表
    else:
        try:
            number_list = number.split(',')
            ll = []
            for j in number_list:
                musics_list3 = LL[int(j) - 1]  # 等于歌曲索引列表
                ll.append(musics_list3)
            return ll  # 等于序列号 返回列表序列号对应值列表
        except:
            print('输入错误,请重新选择')
            get_song_mv(keyword)  # 非序列号重新输入

def kugou_hash(mv_hash):  # 传入MV哈希值 返回KEY值
    m = hashlib.md5()  # 哈希 md5加密
    # song_hash_upper=mv_hash.upper()#大写
    kugou_slat = 'kugoumvcloud'  # 盐
    m.update((mv_hash + kugou_slat).encode("utf8"))  # 哈希值+盐
    key = m.hexdigest()
    return key  # 返回key值

def mv_api(mv_hash, key):  # 访问单个MV页面 返回MV地址 画质
    mv_api_url = 'http://trackermv.kugou.com/interface/index/cmd=100&hash={}&key={}&pid=6&ext=mp4&ismp3=0'.format(
        mv_hash, key)
    # print('正在访问Mv_api页面：{}'.format(mv_api_url))
    r = get_one_page(mv_api_url)
    # print(r.text)
    rq = re.findall(r'"rq":{"hash":".*?mp4"}', r, re.S)  # 找1080
    sq = re.findall(r'"sq":{"hash":".*?mp4"}', r, re.S)  # 找720
    hd = re.findall(r'"hd":{"hash":".*?mp4"}', r, re.S)  # 找540
    sd = re.findall(r'"sd":{"hash":".*?mp4"}', r, re.S)  # 找432
    if rq != []:  # 如果有1080
        mv_url_real = re.findall(r'"downurl":"(.*?)"}', rq[0], re.S)  # 1080MV真实地址
        mv_url = mv_url_real[0].replace('\\', '')
        image_quality = '_1920_1080'
    else:  # 没有1080
        if sq != []:  # 如果有1280
            mv_url_real = re.findall(r'"downurl":"(.*?)"}', sq[0], re.S)  # 720MV真实地址
            mv_url = mv_url_real[0].replace('\\', '')
            image_quality = '_1280_720'
        else:  # 没有1280
            if hd != []:  # 如果有540
                mv_url_real = re.findall(r'"downurl":"(.*?)"}', hd[0], re.S)  # 540MV真实地址
                mv_url = mv_url_real[0].replace('\\', '')
                image_quality = '_960_540'
            else:  # 没有540
                mv_url_real = re.findall(r'"downurl":"(.*?)"}', sd[0], re.S)  # 432MV真实地址
                mv_url = mv_url_real[0].replace('\\', '')
                image_quality = '_768_432'
    return mv_url, image_quality  # 返回真实MV地址,画质

def mv_down(folder_name, mv_url, title, image_quality):  # 传入地址, 文件名 下载文件
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        mv = s.get(mv_url, headers=headers, timeout=15)
        mv.raise_for_status()  # 状态码 如果不是200则报错
        print(title)
        print('正在访问Mv真实页面：{}'.format(mv_url))
        with open(folder_name + '《' + title + '》_ ai尚音乐'  + ".mp4", "wb")as fp:
            fp.write(mv.content)
    except Exception as e:
        t = time.strftime('%Y/%m/%d %H:%M:%S %a')  # 时间格式化
        with open(r'./kugou/Exception.txt', 'a+', encoding='utf-8') as f:
            f.write('time:{}\n\nurl:{}\n\n{}\n\n'.format(t, mv_url, e))

def mv_main(keyword, folder_name):#mv 函数
    ll = get_song_mv(keyword)  # 传入搜索值 返回列表
    z = 0
    for i in ll:
        print(i)
        title, mv_hash = i[0], i[1]  # 标题 ，哈希值
        key = kugou_hash(mv_hash)  # 传入哈希值  返回KEY值
        mv_url, image_quality = mv_api(mv_hash, key)  # 传入哈希值 key值 返回真实地址 画质
        mv_down(folder_name, mv_url, title, image_quality)  # 传入文件夹名 真实地址 标题 画质 下载MV
        z += 1
        print('{} 下载完成,剩余：{},画质：{}'.format(title, (len(ll) - z), image_quality))


def voice_search(keyword):#根据关键字搜索歌曲
    search_url = 'http://songsearch.kugou.com/song_search_v2?keyword={}page=1'.format(keyword)
    # 这里需要判断一下，ip与搜索字段可能会限制搜索，total进行判断
    total = json.loads(get_one_page(search_url))['data']['total']
    if total != 0:
        search_total_url = search_url + '&pagesize=%d' % total
        music_list = json.loads(get_one_page(search_total_url))['data']['lists']#歌曲列表
        for i in range(len(music_list)):
            print(str(i + 1) + ".>>>" + str(music_list[i]['FileName']).replace('<em>', '').replace('</em>', ''))
        number = input("\n请输入要下载的歌曲序号,以英文','号分隔,如:1,3 --（输入-1退出程序）(回车下载全部): ")
        musics_list1 = voice_musics_hash(music_list)#歌曲信息列表
        if number == '':
            musics_list2 = musics_list1#等于全部歌曲信息列表
            return musics_list2
        elif number == '-1':
            exit()
        else:
            try:
                number_list=number.split(',')
                musics_list2=[]
                for j in number_list:
                    musics_list3 = musics_list1[int(j) - 1]#等于歌曲索引列表
                    musics_list2.append(musics_list3)
                return musics_list2
            except:
                print('输入错误')
                voice_search(keyword)
    else:
        return None

def voice_musics_hash(music_list):#歌曲信息列表
    music_items = []
    for music in music_list:
        item = []
        if music['SQFileHash'] != '0' * 32 and music['SQFileHash'] != '':
            item.append(music['SQFileHash'])  # 歌曲无损hash
            item.append('flac')
            item.append('无损')
        else:
            if music['HQFileHash'] != '0' * 32 and music['HQFileHash'] != '':
                item.append(music['HQFileHash'])  # 歌曲高品hash
                item.append('mp3')
                item.append('高品')
            else:
                if music['FileHash'] != '0' * 32 and music['FileHash'] != '':
                    item.append(music['FileHash'])  # 歌曲普通hash
                    item.append('mp3')
                    item.append('普通')
                else:
                    print('该歌曲酷狗无版权')
                    continue
        item.append(clean_txt(music['FileName'].replace('<em>', '').replace('</em>', '')))  # 歌手—歌曲
        music_items.append(item)
    return music_items

def v2_md5(Hash):  # 用于生成key,适用于V2版酷狗系统
    return hashlib.md5((Hash + 'kgcloudv2').encode('utf-8')).hexdigest()

def voice_main(keyword, folder_name):#音频函数
    music_list = voice_search(keyword)#搜索关键词
    if music_list is not None:
        y = 0
        for music in music_list:
            Hash = str.lower(music[0])#小写哈希值
            key_new = v2_md5(Hash)  # 生成v2系统key
            Music_api_1 = 'http://trackercdnbj.kugou.com/i/v2/?cmd=23&pid=1&behavior=download'
            DownUrl = Music_api_1 + '&hash=%s&key=%s' % (Hash, key_new)#拼接歌曲接口地址
            try:
                music.append(json.loads(get_one_page(DownUrl))['url'])
                downloud_song(folder_name, music)#下载歌曲
                y += 1
                print('{} 下载完成,剩余:{},音质：{}'.format(music[3], len(music_list) - y, music[2]))
            except:
                y += 1
                print('解析错误，剩余：{}'.format(len(music_list) - y))

def downloud_song(folder_name, music):#下载歌曲 voice
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        mp3 = s.get(music[4], headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)  # 访问真实地址 下载歌曲
        with open(folder_name + '\\' + music[3] + "." + music[1], "wb")as f:
            f.write(mp3.content)
    except Exception as e:
        t = time.strftime('%Y/%m/%d %H:%M:%S %a')  # 时间格式化
        with open(r'./kugou/Exception.txt', 'a+', encoding='utf-8') as f:
            f.write('time:{}\n\nurl:{}\n\n{}\n\n'.format(t, music, e))


def choice():  # 选择下载歌曲或者MV
    x = input('输入序列号选择：1.>>搜索歌曲 mp3/flac  2.>>搜索MV mp4 》》》')
    if x == '2' or x == '1':
        return x
    else:
        print('输入错误,重新输入')
        choice()

def main():
    x = choice()
    # keyword= clean_txt('Taylor Swift - Style')#测试外文
    # keyword= clean_txt('Stellar - 찔려')#测试外文
    # keyword= clean_txt('花澤香菜 - 恋愛サーキュレーション')#测试外文
    # keyword =  clean_txt("SING女团 - 寄明月")  # 测试歌名
    # keyword = clean_txt('七朵组合')# 测试歌手
    keyword = clean_txt(input('输入歌手或歌名》》》'))  # 正式
    folder_name = r'/kugou/' % keyword  # 文件名
    create_folder(folder_name)  # 创建文件夹
    if x == '1':  # 1调用mpc_main 函数
        voice_main(keyword, folder_name)
    elif x == '2':  # 等于2 调用 mv_main 函数
        mv_main(keyword, folder_name)
    print('下载完成')


class MySpider(scrapy.Spider):
    # 设置name
    name = "sgd"

    def start_requests(self):
        urls = []
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456789',
            'database': 'scrapy',
            'charset': 'utf8'
        }
        conn = pymysql.connect(**dbparams)
        cursor = conn.cursor(DictCursor)
        query_sql = """
                      select * from sougoumv;
                      """
        # 执行插入数据到数据库操作
        cursor.execute(query_sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for i in rows:
            id=i["id"]
            id = i["id"]
            title = i["title"]
            print(id)
            shangxue = "https://www.kugou.com/mvweb/html/mv_{}.html".format(id)
            yield scrapy.Request(url=shangxue, meta={'id': id, 'title': title}, callback=self.parse)
            break
        # for i in range(1,100):
        #     print(i)
        #     new_url = "https://www.kugou.com/mvweb/html/index_9_%s.html" % (str(i))
        #     urls.append(new_url)
        # print(urls)
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
    # 编写爬取方法
    def parse(self, response):
        print("-"*100)
        idx = response.meta['id']
        title = response.meta['title']
        print(idx)
        mv_hash = response.xpath("/html/body/div[@class='frame mv_page']/div[@class='publicShareImgBox']/img/@_src").extract()
        mv_hash=mv_hash[0]
        print(mv_hash)
        # "http://imge.kugou.com/mvpic/6d/d1/6dd1cbd70e98d5f31caccd8d41fc0d59.jpg"
        array=mv_hash.split("/")
        laststr=array[len(array) - 1]
        print(laststr)
        mv_hashArray=laststr.split(".")
        mv_hash=mv_hashArray[0]
        print(mv_hash)
        key = kugou_hash(mv_hash)  # 传入哈希值  返回KEY值
        mv_url, image_quality = mv_api(mv_hash, key)  # 传入哈希值 key值 返回真实地址 画质

        folder_name = r'/Users/leili/Desktop/sougou/sougou/kugou/' # 路径
        create_folder(folder_name)  # 创建文件夹

        mv_down(folder_name, mv_url, title, image_quality)  # 传入文件夹名 真实地址 标题 画质 下载MV

        # item = SougouItem()
        # print(tubimages)
        # for idx, val in enumerate(webs):
        #     ahref=val.extract()
        #     id1 = ahref.replace("/mvweb/html/mv_", "")
        #     id = id1.replace(".html", "")
        #     print(id)
        #     weburl = "https://m3ws.kugou.com/mv/{}.html".format(id)
        #     print(weburl)
        #     title=titles[idx]
        #     print(title)
        #     thumb_url = tubimages[idx]
        #     print(thumb_url)
        #     item['id'] = id
        #     item['title'] = title
        #     item['web_url'] = weburl
        #     item['thumb_url'] =thumb_url
        #     yield item

        print("+" * 100)
