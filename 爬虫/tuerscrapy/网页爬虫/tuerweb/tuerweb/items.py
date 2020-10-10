# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TuerwebItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    pinyin = scrapy.Field()
    pc_instruction = scrapy.Field()
    gif = scrapy.Field()
    pic = scrapy.Field()
    pass


class GushiItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    gif = scrapy.Field()
    pic = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    md5 = scrapy.Field()
    play_num = scrapy.Field()
    introduction = scrapy.Field()
    type = scrapy.Field()
    pass

class HuibenItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    pics = scrapy.Field()
    introduction = scrapy.Field()
    img = scrapy.Field()
    meta_url = scrapy.Field()
    pass

class ZtItem(scrapy.Item):
    id = scrapy.Field()
    value = scrapy.Field()
    type = scrapy.Field()
    subtitle = scrapy.Field()
    title = scrapy.Field()
    pic = scrapy.Field()
    gif = scrapy.Field()
    instruction = scrapy.Field()
    charge = scrapy.Field()
    source_num = scrapy.Field()
    meta_url = scrapy.Field()

    pass
