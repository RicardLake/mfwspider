# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors
from maatt.mafengwoatt.mafengwoatt import settings
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MysqlPipelineTwo(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

        return item
    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
            insert into attraction(city, att_name, location ,detail,com_num, pos_num,mod_num,neg_num)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (item['city'],
                     item['att_name'],
                     item['location'],
                     item['detail'],
                     item['comment_num'],
                     item['pos_comment'],
                     item['mod_comment'],
                     item['neg_comment']))

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)



class MafengwoattPipeline(object):
    def __init__(self):
        #连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=False)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        try:
            # 查重处理
            self.cursor.execute(
                """select * from attraction where att_name = %s""",
                item['att_name'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()

            # 重复
            if repetition:
                pass

            else:
                # 插入数据
                self.cursor.execute(
                    """insert into attraction(city, att_name, location ,detail,com_num, pos_num,mod_num,neg_num)
                    value (%s, %s, %s, %s, %s, %s,%s, %s, %s)""",
                    (item['city'],
                     item['att_name'],
                     item['location'],
                     item['detail'],
                     item['comment_num'],
                     item['pos_commen'],
                     item['mod_comment'],
                     item['neg_comment'])
                )

            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误
            print(error)
        return item









