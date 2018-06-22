import scrapy
from crawler.items import CrawlerItem

class MovieScrapy(scrapy.Spider):
    # 이 3개의 변수는 항상 선언해야한다.
    name = "NaverMovie"
    allow_domain =["https://movie.naver.com"]
    start_urls =[
        "https://movie.naver.com/movie/running/current.nhn"
    ]

    # 링크를 가져오는 함수
    # start_urls가 request를 해서 나온
    def parse(self, response):
        links = response.xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li/dl/dt/a/@href')[:10].extract()
        for link in links:   #풀도메인으로 재작성
            link = response.urljoin(link)
            yield scrapy.Request(link,callback=self.parse_page_contents) #링크 하나하나를 보내서 response를 받음

    def parse_page_contents(self, response):
        item = CrawlerItem()
        item["title"] = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3/a[1]/text()').extract()[0]
        try:
            item["count"] = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[5]/div/p[2]/text()').extract()[0]
        except:
            item["count"] = "정보없음."
        yield item
