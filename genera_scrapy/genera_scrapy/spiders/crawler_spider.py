# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlerSpiderSpider(CrawlSpider):
    name = 'mongodb'
    allowed_domains = ['runoob.com']
    start_urls = ['http://www.runoob.com/mongodb/mongodb-tutorial.html']

    rules = (
        # Rule(LinkExtractor(allow=r'/mongodb'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/mongodb'), callback='parse_item'),
    )

    def parse_item(self, response):
        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()


        print(response.text)
        paths = urlparse(response.url).path
        url_name = paths[len(paths)-1]
        file_name = './download/'+paths+'.html'
        with open(file_name,'wb') as f:
            f.write(response.body)

