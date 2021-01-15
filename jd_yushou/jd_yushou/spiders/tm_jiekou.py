import scrapy

from urllib import parse
import json
import time

class TmJiekouSpider(scrapy.Spider):

    handle_httpstatus_list = [403,302]
    name = 'tm_jiekou——spider'
    start_urls = [
        'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.13.62647852D7nKW1&id=532580297331&skuId=4617297734014&user_id=2081948193&cat_id=2&is_b=1&rn=7858c9cb6057c6a20e33b8bef4029d0c',
        'https://login.taobao.com/jump?target=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm%3Da220o.1000855.0.da321h.6ef918be2Cn7Fj%26id%3D563233800548%26skuId%3D4508086770457%26tbpm%3D1',
        'https://pass.tmall.com/add?cookie2=15bd17e1dd24628378c16d704d543b94&t=77b94c2c4182f4461d6e3826da34c684&_tb_token_=eb6a69557ee33&tmsc=1610334410419000&opi=11.82.29.90&pacc=8hSliq5dd0y_aLMbP9jtpA==&target=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm%3Da220o.1000855.0.da321h.6ef918be2Cn7Fj%26id%3D563233800548%26skuId%3D4508086770457%26tbpm%3D1',
    ]

    headers = {
        "User-Agent": 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.141Safari/537.36',
    }
    def start_requests(self):
        skuid = '3408088338019'
        idd = '521201233938'
        url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.13.62647852D7nKW1&id={0}&skuId={1}'.format(idd,skuid)
        yield scrapy.Request(
            url=url,
            callback=self.get_cookie,
            dont_filter=True,
        )

    def get_cookie(self, response):
        url = response.headers.get('Location').decode('utf-8')
        time.sleep(1)
        yield scrapy.Request(
            url=url,
            callback=self.get_cookie2,
            dont_filter=True,
        )
    def get_cookie2(self, response):
        print(response.text)
        new_cookie = {}

        for bit in response.headers.getlist('Set-Cookie'):
            str = bit.decode('utf-8')
            new_cookie[str.split(';')[0].split('=')[0]] = str.split(';')[0].split('=')[1]
        Location = response.headers.get('Location').decode('utf-8')
        yield scrapy.Request(
            url=Location,
            callback=self.set_cookie,
            headers=self.headers,
            cookies=new_cookie,
            dont_filter=True,
        )
    def set_cookie(self,response):
        skuid = '3408088338019'
        idd = '521201233938'
        url = response.headers.get('Location').decode('utf-8')
        # print(response.headers)
        yield scrapy.Request(
            url=url,
            callback=self.get_zhuye,
            headers=self.headers,
            dont_filter=True,
        )

    def get_zhuye(self, response):
        print(response.text)
        # print(response.request.headers)
        url = self.get_url(response.text)
        url = response.headers.get('Location').decode('utf-8')
        yield scrapy.Request(
            # url='http:'+url,
            # callback=self.get_price,
            url=url,
            callback=self.get_zhuye,
            headers=self.headers,
            dont_filter=True,
        )
    def get_price(self,response):
        # print(response.text)
        pass
    def get_url(self,text):
        ls = text.split('\n')
        url = ls[13].split('\'')
        return url[1]
