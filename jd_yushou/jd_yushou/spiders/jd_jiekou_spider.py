import scrapy
import random
import re
from urllib.parse import quote
import json

class JdJiekouSpiderSpider(scrapy.Spider):
    name = 'jd_jiekou_spider'
    start_urls = ['http://www.baidu.com']
    headers = {
        'referer': 'https://search.jd.com/',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88Safari/537.36',
        }
    def parse(self, response):
        url = "https://item.jd.com/{0}.html"
        skuId = "100009993680"
        yield scrapy.Request(url=url.format(skuId),
                             callback=self.get_shopid,
                             meta={"skuId":skuId},
                             dont_filter=True,
                             headers=self.headers
                             )

    def get_shopid(self,response):
        skuId = response.meta['skuId']
        shopId = response.xpath('//div[@class="follow J-follow-shop"]/@data-vid').get()
        catids = response.xpath('//body/@class').get()
        cat_list = catids.split(' ')
        cat = self.get_cat(cat_list)
        paramJson = re.findall("paramJson: '(.*?)' ,", response.text)
        if paramJson!= []:
            paramJson = paramJson[0]
        base_url = "https://item-soa.jd.com/getWareBusiness?callback=jQuery{0}" \
                   "&skuId={1}&cat={2}&" \
                   "area=1_72_55657_0&shopId={3}&venderId={4}" \
                   "&paramJson={5}&num=1"
        random_int = random.randint(1000000, 9999999)
        url = base_url.format(str(random_int), skuId, quote(cat),
                              shopId, shopId, quote(paramJson))
        yield scrapy.Request(url=url,
                             callback=self.get_price,
                             meta={
                                 "skuId": skuId,
                                 'random_int': random_int,
                                   },
                             dont_filter=True,
                             headers=self.headers
                             )

    def get_cat(self,cat_list):
        new_list = []
        for i in cat_list:
            if "cat" in i:
                flist = i.split('-')
                if flist[2] != "":
                    new_list.append(flist[2])
        return ','.join(new_list)

    def get_price(self,response):
        random_int = response.meta['random_int']
        text = response.text.replace('jQuery{0}('.format(str(random_int)), '').replace(')', '')
        data_json = json.loads(text)
        # 预售价
        tailMoney = self.get_content(data_json, ['YuShouInfo', 'tailMoney'], 'text')
        # 定金
        yuShouDeposit = self.get_content(data_json, ['YuShouInfo', 'yuShouDeposit'], 'text')
        print(tailMoney)
        print(yuShouDeposit)

    def get_content(self,data_json, guize, rt_lx):
        '''

        :param data_json:
        :param guize:
        :param rt_lx: 返回类型
        :return:
        '''
        if rt_lx == "text":
            s = data_json
            try:
                for i in guize:
                    s = s.get(i)
            except Exception as e:
                print(e)
                return ""
            else:
                return str(s)
        elif rt_lx == "list":
            s = data_json
            try:
                for i in guize:
                    s = s.get(i)
            except Exception as e:
                print(e)
                return []
            else:
                return s
        elif rt_lx == "json":
            s = data_json
            try:
                for i in guize:
                    s = s.get(i)
            except Exception as e:
                print(e)
                return {}
            else:
                return s