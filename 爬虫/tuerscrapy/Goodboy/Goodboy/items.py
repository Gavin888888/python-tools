# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class specialList(scrapy.Item):
    # 定义我们需要的存储数据字段
    id = scrapy.Field()
    name = scrapy.Field()
    free_num = scrapy.Field()
    type = scrapy.Field()
    dateline = scrapy.Field()
    pic = scrapy.Field()
    gif = scrapy.Field()
    subtitle = scrapy.Field()
    play_num = scrapy.Field()
    source_num = scrapy.Field()
    charge = scrapy.Field()
    playNum = scrapy.Field()
    formatPlayNum = scrapy.Field()
    pass

class audioItem(scrapy.Item):
    fatherid = scrapy.Field()
    id = scrapy.Field()
    storyType = scrapy.Field()
    pic = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    md5 = scrapy.Field()
    play_num = scrapy.Field()
    uploader = scrapy.Field()
    playNum = scrapy.Field()
    formatPlayNum = scrapy.Field()
    pass