# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlite3 import connect

class sqlite_db(object):
    def __init__(self):
        self.conn = connect('SXVT.sqlite')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists jobs("id" INTEGER PRIMARY KEY AUTOINCREMENT,url varchar(128) , company varchar (32), job_title varchar (32), job_salary varchar (32), job_address varchar (64), job_describe text) ')
        self.conn.commit()
    def search_url(self,url_str):
        result = self.cursor.execute("select url from jobs where url='{}'".format(url_str))
        return result.fetchone()



class ZhilianspiderPipeline(object):

    def __init__(self):
        self.sqlite_db = sqlite_db()
        self.conn = self.sqlite_db.conn
        self.cursor = self.sqlite_db.cursor
    def process_item(self, item, spider):

        insert_detail = [(
            item['url'],
            item['company'],
            item['job_title'],
            item['job_salary'],
            item['job_address'],
            item['job_describe'],
        )]
        self.cursor.executemany('INSERT INTO jobs(url,company,job_title,job_salary,job_address,job_describe) VALUES (?,?,?,?,?,?)',insert_detail)
        self.conn.commit()
        return item
