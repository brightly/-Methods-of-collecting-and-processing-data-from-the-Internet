import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/?stype=0']


    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        print()
        url = response.url
        name = response.xpath("//h1/text()").get()
        price_f = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        price_s = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        author = response.xpath("//a[@data-event-label='author']/text()").get()
        rate = response.xpath("//div[@id='rate']/text()").get()
        yield JobparserItem(url=url, name=name, price_f=price_f, price_s=price_s, author=author, rate=rate)




