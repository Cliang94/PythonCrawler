# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from pymongo import MongoClient
from qcwy.random_proxies import MongoCache_qcwy



class QcwyPipeline(object):

    def __init__(self):
        self.conn = sqlite3.connect('zhaopin.db')
        self.cours = self.conn.cursor()
        self.cours.execute('create table if not exists qcwy("id" INTEGER PRIMARY KEY AUTOINCREMENT,"job_title" varchar(64),"job_details" text, "company" varchar(64),"workplace" varchar(64),"pay" varchar(64) )')
        self.conn.commit()
        self.db = MongoCache_qcwy()

    def process_item(self, item, spider):

        # self.url_db['url'] = item['url']
        if item['url'] not in self.db:
            insert_sql = "insert into qcwy(job_title, job_details, company, workplace, pay) values('{}','{}','{}','{}','{}')".format(item['job_title'],item['job_details'] ,item['company'], item['workplace'], item['pay'])
            self.cours.execute(insert_sql)
            self.conn.commit()
            return item

"""

conn = sqlite3.connect('D:/Document/08-pachong/Scrapy爬虫/qcwy/qcwy/zhaopin.db')

curs = conn.cursor()

curs.execute("select * from qcwy where job_title='算法工程师' and commpany='河南紫光物联技术有限公司'")

"""




