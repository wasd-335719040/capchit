import scrapy
import random
import re
from urllib.parse import quote
import json


class TmJiekouSpiderSpider(scrapy.Spider):
    name = 'tm_jiekou_spider'
    headers = {
        # 'Connection': 'keep-alive',
        'referer': 'https://list.tmall.com/',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88Safari/537.36',
    }

    def start_requests(self):
        url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.16.27297852I4AqPv&id=42972619574&skuId=4088756263107&user_id=2248304671&cat_id=2&is_b=1&rn=b8c9e1aff1a904cc3162e0922978c7dd'

        yield scrapy.Request(url=url,
                             callback=self.get_price,
                             headers=self.headers,
                             )

    def get_price(self,response):
        print(123)
        print(response.text)
        pass