import requests
import execjs
from lxml import etree
import json
headers = {
        # 'Host':"detail.tmall.com",
        'referer': 'https://www.tmall.com/?spm=a2233.7711963.a2226mz.1.49b57fb8teJNTn',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88Safari/537.36',
    }
# s=requests.session()
url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.16.27297852I4AqPv&id=42972619574&skuId=4088756263107&user_id=2248304671&cat_id=2&is_b=1&rn=b8c9e1aff1a904cc3162e0922978c7dd'
response = requests.get(url=url, headers=headers, verify=False, timeout=10, allow_redirects=True)
xp = etree.HTML(response.text)
lf = xp.xpath('/html/head/script/text()')[0]
url_str = lf.split('\n')[3]
lis = url_str.split('\'')
print(lis[1])
base_url = 'https:'

response = requests.get(url=base_url+lis[1]+'&cat_id=2', headers=headers, verify=False, timeout=10, allow_redirects=True)
jsons = json.loads(response.text)

print(jsons)

