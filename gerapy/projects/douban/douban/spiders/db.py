import scrapy


class DbSpider(scrapy.Spider):
    name = "db"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        print('ua===>',response.request.headers['User-Agent']) 
        # 拿取电影节点
        move_list = response.css('ol.grid_view > li')
        for movie in move_list:
            item = {}
            # 电影名称
            item['name'] = movie.css('span[class="title"]').css('::text').get()
            # 电影描述
            item['quote'] = movie.css('span[class="inq"]').css('::text').get()
            # 电影评分
            item['rating'] = movie.css('span[class="rating_num"]').css('::text').get()
            # print(item)
            yield item
        # 构建下一页url
        next_url = response.css('span.next > a').css('::attr(href)').get()
        if next_url != None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url)
    
