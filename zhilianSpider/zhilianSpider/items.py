# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 公司名称
    company = scrapy.Field()
    # 职位名称
    job_title = scrapy.Field()
    # 职位薪资
    job_salary = scrapy.Field()
    # 工作地址
    job_address = scrapy.Field()
    # 岗位职责
    job_describe = scrapy.Field()
    # url
    url = scrapy.Field()

