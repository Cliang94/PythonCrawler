from scrapy.spider import Spider
from scrapy import Request

from urllib.parse import urljoin,urlparse
from qcwy.items import QcwyItem
from qcwy.random_proxies import MongoCache_qcwy


class qcwySpider(Spider):
    """
    前程无忧
    """
    # name = 'qcwy'
    # def __init__(self):
    #     super(qcwySpider, self).__init__()
    #     self.url_base = 'https://search.51job.com/list/170200,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    #     self.urls = [self.url_base.format(i) for i in range(1,5)]
    #
    #

    # def start_requests(self):
    #     for url_str in self.urls:
    #         yield Request(url=url_str,callback=self.parse)


    name = 'qcwy'
    # allowed_domains = ['https://search.51job.com']
    # url_base = 'https://search.51job.com/list/170200,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    # url_base = 'https://search.51job.com/list/170200,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    start_urls = ['https://search.51job.com/list/170200%252C020000,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(i) for i in range(3,200)]

    def parse(self, response):
        db = MongoCache_qcwy()
        urls = response.xpath('//*[@id="resultList"]/div/p/span/a/@href').extract()
        for url in urls:
            yield Request(url,callback=self.parse)

        job_title = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()').extract_first().strip()
        company = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()').extract_first().strip()
        workplace = response.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()').extract()[-1].strip()
        pay = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract_first()
        job_list1 = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/div[1]/p/span/text()').extract()
        job_list2 = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()').extract()
        job_details = ''
        for i in job_list2:
            job_details += i
        job_details += ','
        for i in job_list1:
            job_details += i



        # 职能类别  /html/body/div[3]/div[2]/div[3]/div[1]/div/div[1]/p/span
        # 岗位描述  /html/body/div[3]/div[2]/div[3]/div[1]/div/p

        item = QcwyItem()
        item['job_title'] = job_title.strip()
        item['company'] = company
        item['workplace'] = workplace
        item['pay'] = pay
        item['job_details'] = job_details
        item['url'] = response.url
        # print('---'*100)
        # print(response.url)
        yield item



    def data(self,response):
        data = response.xpath()
























