# -*- coding: utf-8 -*-
import scrapy
from maatt.mafengwoatt.mafengwoatt.items import MafengwoattItem
from selenium import webdriver
import time



class JdattSpider(scrapy.Spider):
    name = 'jdatt'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/jd/21536/gonglve.html']

    @staticmethod
    def get_urls(self,):
        fp=open("href.txt",'wb')
        driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

        driver.get("http://www.mafengwo.cn/jd/21536/gonglve.html")
        hrefs = driver.find_elements_by_xpath('//ul[@class="scenic-list clearfix"]//li//a')

        for href in hrefs:
            poi_url = href.get_attribute("href")
            fp.write(poi_url.encode("utf8")+b'\n')
        page_num = int(driver.find_element_by_xpath("//span[@class='count']//span[1]").text)
        for i in range(1,page_num):
            driver.find_element_by_xpath(u"//div[@class='m-pagination']//a[@title='后一页']").click()
            time.sleep(3)
            hrefs = driver.find_elements_by_xpath('//ul[@class="scenic-list clearfix"]//li//a')
            for href in hrefs:
                poi_url = href.get_attribute("href")
                fp.write(poi_url.encode("utf8") + '\n')
        fp.close()
        driver.close()
    def parse(self, response):
        '''
        #获取每个景点的链接
        att_list=response.xpath('//ul[@class="scenic-list clearfix"]//li')
        for att in att_list:
            href='http://www.mafengwo.cn'+att.xpath('./a/@href').extract()[0]
            yield scrapy.Request(href,callback=self.parse_att)


        driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.get("http://www.mafengwo.cn/jd/21536/gonglve.html")
        content = driver.page_source.encode('utf-8')
        for i in range(2,7726):
            next_page=driver.find_element_by_xpath("//a[@title='后一页']")
            next_page.click()

        driver.close()
        '''


    def parse(self, response):
        att_item = MafengwoattItem()
        att_item['city'] = response.xpath("//div[@class='item']//span//a/text()").extract()[0]
        att_item['att_name'] = response.xpath("//div[@class='title']//h1/text()").extract()[0]
        att_item['detail'] = response.xpath("//div[@class='summary']/text()").extract()[0].strip()
        att_item['location'] = response.xpath("//div[@class='mod mod-location']//p/text()").extract()[0]
        att_item['comment_num'] = response.xpath("//div[@class='mod mod-reviews']//span//em/text()").extract()[0]
        if att_item['comment_num']=='0':
            att_item['pos_comment']='0'
            att_item['mod_comment']='0'
            att_item['neg_comment']='0'
        else:
            att_item['pos_comment'] = response.xpath(
                "//div[@class='review-nav']//li[@data-category='13']//span[@class='num']/text()").extract()[0]
            att_item['mod_comment'] = response.xpath(
                "//div[@class='review-nav']//li[@data-category='12']//span[@class='num']/text()").extract()[0]
            att_item['neg_comment'] = response.xpath(
                "//div[@class='review-nav']//li[@data-category='11']//span[@class='num']/text()").extract()[0]
        yield att_item



