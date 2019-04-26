# -*- coding: utf-8 -*-
import scrapy
from maatt.mafengwoatt.mafengwoatt.items import MafengwoattItem
from selenium import webdriver
import time



class JdattSpider(scrapy.Spider):
    name = 'jdatt'
    allowed_domains = ['mafengwo.cn']
    fr = open(r"D:\PyCharm\maatt\mafengwoatt\mafengwoatt/href.txt")
    urls=list()
    for i in fr.readlines():
        urls.append(i.strip())
    start_urls = urls[13290:-1]
    def parse(self, response):
        att_item = MafengwoattItem()
        att_item['city'] = response.xpath("//div[@class='item']//span//a/text()").extract()[0]
        att_item['att_name'] = response.xpath("//div[@class='title']//h1/text()").extract()[0]
        try:
            att_item['detail'] = response.xpath("//div[@class='summary']/text()").extract()[0].strip()
        except:
            att_item['detail'] = ""
        att_item['location'] = response.xpath("//div[@class='mod mod-location']//p/text()").extract()[0]
        att_item['comment_num'] = response.xpath("//div[@class='mod mod-reviews']//span//em/text()").extract()[0]
        try:
            att_item['pos_comment'] = response.xpath(
                "//div[@class='review-nav']//li[@data-category='13']//span[@class='num']/text()").extract()[0]
        except:
            att_item['pos_comment']="（0条）"
        try:
            att_item['mod_comment'] = response.xpath(
                "//div[@class='review-nav']//li[@data-category='12']//span[@class='num']/text()").extract()[0]
        except:
            att_item['mod_comment']="（0条）"
        try:
            att_item['neg_comment'] = response.xpath(
                "//div[@class='review-nav']//li[@data-category='11']//span[@class='num']/text()").extract()[0]
        except:
            att_item['neg_comment']="（0条）"
        yield att_item

