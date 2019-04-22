# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwoattItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city=scrapy.Field()
    att_name=scrapy.Field()
    detail=scrapy.Field()
    location=scrapy.Field()
    comment_num=scrapy.Field()
    pos_comment=scrapy.Field()
    mod_comment=scrapy.Field()
    neg_comment=scrapy.Field()
