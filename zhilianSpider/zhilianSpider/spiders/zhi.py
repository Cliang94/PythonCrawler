from scrapy.spider import Spider
from scrapy import Request
from zhilianSpider.items import ZhilianspiderItem as zl
from zhilianSpider.pipelines import sqlite_db as job_db
from hashlib import md5
from random import choice


class JobProfile(object):
    """
    工作描述类，模型类，用来存储解析结果，以及进行一些简单的数据清晰

    """
    def __init__(self):
        self.job_url = ''
        self.job_saray = ''
        self.job_ = ""
    def __str__(self):
        return 'job_url:::::{}<br>job_saray::::{}'.format(self.job_url,self.job_saray)

    # 限制薪资待遇范围
    def salary_limit(self):
        return True

    # 限制地区
    def aere_limit(self):
        return True

    # 限制工作内容
    def job_desc_limit(self):
        return True


class url_md5(object):
    """
    url 的 md5 加密即校验
    """

    def __init__(self):
        self.md5 = md5()
        self.db = job_db()


    def url_md5_set(self,url_str):
        m = md5()
        m.update(url_str.encode('utf-8'))
        return m.hexdigest()

    def check_url_str(self,url_str):
        md5_url = self.url_md5_set(url_str)
        result = self.db.search_url(md5_url)

        if result:
            return False
        else:
            return True






class zhilianSpider(Spider):
    name = 'zhilian'

    def __init__(self):
        super(zhilianSpider, self).__init__()
        self.md5_url = url_md5()

    def start_requests(self):
        urls = ['https://sou.zhaopin.com/?pageSize=60&jl=538&kw=python&kt=3']
        for url in urls:
            yield Request(url, callback=self.parse, meta={'page': '1'})


    def parse(self, response):
        # jobs = response.css('div.listItemBox-wrapper').extract()

        job_urls = response.xpath('//div[@class="jobName"]/a[@href]/@href').extract()
        page_index = response.css('span.page-index').extract()
        for url in job_urls:

            if self.md5_url.check_url_str(url):
                yield Request(url=url, callback=self.job_detail, meta={'page': '0'})
        if len(page_index) > 0:
            url__ = ['http://www.baidu.com/{}/'.format(i) for i in range(150)]
            for i in url__:
                yield Request(url=i,callback=self.parse,meta={'page':'2'})





    def job_detail(self, response):
        """
        解析职位详细页
        公司名称：company   response.xpath('//div[@class="fl"]/h2/a/text()').extract()
        职位名称：title     response.xpath('//div[@class="fl"]/h1/text()').extract_first()
        职位薪资：salary    response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract_first()
        工作地址：address   response.xpath('//div[@class="tab-inner-cont"]/h2/text()').extract_first()
        岗位职责: describe  response.xpath('//div[@class="box pre"]/text()').extract()   list
                           response.xpath('//div[@class="tab-inner-cont"]/p/text()').extract()
        工作网址： url      response.url
        :param response:
        :return:
        """
        if 'xiaoyuan' in response.url:
            company = response.xpath('//div[@class="cJobDetailInforWrap"]/ul/li/a[@href]/text()').extract_first().strip()
            job_title = response.xpath('//h1[@id="JobName"]/text()').extract_first().splitlines()[-1].strip()
            job_salary = response.xpath('//li/strong/text()').extract_first().strip()
            job_address = response.xpath('//li[@id="currentJobCity"]/@title').extract_first().strip()
            if not job_address:
                job_address = response.xpath('//h2/text()').extract_first().strip()
            desc = response.xpath('//div[@class="cJob_Detail f14"]/p[@class="mt20"]/text()').extract()
            if len(desc) < 1:
                desc = response.xpath('//div[@class="tab-inner-cont"]/p/text()').extract()
                if len(desc) < 1:
                    desc = response.xpath('//div[@class="pos-ul"]/p/span/text()').extract()
                    if len(desc) < 1:
                        de = response.xpath('//div[@style="FONT-SIZE: 12px"]/strong/text()').extract_first().strip()
                        desc = response.xpath('//div[@style="FONT-SIZE: 12px"]/p/text()').extract()
                        desc.insert(0, de)

        else:
            print(response.url)
            company = response.xpath('//div[@class="company l"]/a/text()').extract_first()
            if not company:
                company = response.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()').extract_first()
                if not company:
                    company = response.xpath('//h2[@onclick]/a/text()').extract_first()
                    if not company:
                        company = '暂无'

            job_title = response.xpath('//h1/text()').extract_first()
            if not job_title:
                job_title = response.xpath('//div[@class="inner-left fl"]/h1/text()').extract_first()
                if not job_title:
                    job_title = '暂无'

            job_salary = response.xpath('//li/strong/text()').extract_first()
            if not job_salary:
                job_salary = '暂无'

            job_address = response.xpath('//p[@class="add-txt"]/text()').extract_first()
            if not job_address:
                job_address = response.xpath('//h2/text()').extract_first()
                if not job_address:
                    job_address = '暂无'

            desc = response.xpath('//div[@class="pos-ul"]/p/text()').extract()
            if not desc:
                desc = response.xpath('//div[@class="tab-inner-cont"]/p/text()').extract()
                if len(desc) < 1:
                    desc = response.xpath('//div[@class="pos-ul"]/p/span/text()').extract()
                    if len(desc) < 1:
                        desc = response.xpath('//td/text()').extract()


        item = zl()
        print('url::::::',response.url)
        item['url'] = self.md5_url.url_md5_set(response.url)
        item['company'] = company.splitlines()[-1].strip()
        item['job_title'] = job_title.splitlines()[-1].strip()
        item['job_salary'] = job_salary.splitlines()[-1].strip()
        item['job_address'] = job_address.strip()
        desc_detail = ''
        for i in desc:
            i = i.strip()
            desc_detail += i
        item['job_describe'] = desc_detail
        yield item
