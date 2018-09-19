# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QcwyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名称
    job_title = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 工作地址
    workplace = scrapy.Field()
    # 薪资
    pay = scrapy.Field()
    # 职位描述
    job_details = scrapy.Field()
    # # url
    url = scrapy.Field()