import logging

from scrapy import Spider,Request,FormRequest
import lxml.html

def parse_form(html):
    """
    找到所有form表单提交的关键字
    :param html:
    :return:
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            }


class CokkiesSpider(Spider):
    name = 'CookiesSpider'
    allowed_domains = ['webscraping.com']
    def start_requests(self):
        return [Request('http://example.webscraping.com/places/default/user/login',headers=headers,callback=self.login)]

    def login(self,response):
        post_data = parse_form(response.text)
        post_data['email'] = 'ccccc@qq.com'
        post_data['password'] = '123qwe'
        # 提交表单信息，登陆使用，相当于post一个url请求
        return [FormRequest(
            'http://example.webscraping.com/places/default/user/login',
            formdata=post_data,headers=headers,
            callback=self.after_login)]
    def after_login(self,response):
        # 登陆成功后第一个下载的种子页    make_requests_from_url 将控制流程交换给scrapy，重新开始爬虫逻辑处理
        return self.make_requests_from_url('http://example.webscraping.com')

    def parse(self, response):
        logging.debug('*'*40)
        logging.debug('response text: %s' % response.text)
        logging.debug('response headers: %s' % response.request.headers)
        logging.debug('response cookies: %s' % response.request.cookies)