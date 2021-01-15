from scrapy.crawler import CrawlerProcess
from jd_yushou.jd_yushou.spiders.tm_jiekou import TmJiekouSpider

process = CrawlerProcess()
process.crawl(TmJiekouSpider)
process.start()