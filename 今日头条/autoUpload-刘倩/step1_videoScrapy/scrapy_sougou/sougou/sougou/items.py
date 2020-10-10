# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SougouItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    weburl = scrapy.Field()
    tumbimage = scrapy.Field()
    mvurl = scrapy.Field()
    localurl = scrapy.Field()
    pass
