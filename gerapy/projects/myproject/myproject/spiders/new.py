#coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from myproject.items import MyprojectItem

class NewSpider(CrawlSpider):
    name = "new"  # 爬虫项目名称
    allowed_domains = ["douban.com"]  # 爬取的域名
    start_urls = ["https://movie.douban.com/top250"]  # 爬取的第一个网址

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = MyprojectItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')

        for movie in movies:
            item['title'] = movie.xpath('div[@class="hd"]/a/span/text()').extract()[0]
            item['star'] = movie.xpath('div[@class="bd"]/div/span[@class="rating_num"]/text()').extract()[0]
            item['critical'] = movie.xpath('div[@class="bd"]/div/span/text()').extract()[1]

            yield item

            next_link = selector.xpath('//span[@class="next"]/link/@href').extract()
            if next_link:  # 第十页是最后一页，没有下一页的链接
                next_link = next_link[0]
                yield Request(self.start_urls[0] + next_link)

