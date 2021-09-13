import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=%D0%BB%D0%B0%D0%BC%D0%B8%D0%BD%D0%B0%D1%82&suggest=true&family=laminat-201709']

    def parse(self, response:HtmlResponse):
        print()
        links = response.xpath("//a[@class='bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp']/@href").getall()
        next_page = response.xpath("//a[@class='bex6mjh_plp o1ojzgcq_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        print()
        url = response.url
        name = response.xpath("//h1/text()").get()
        price_f = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        price_s = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        author = response.xpath("//a[@data-event-label='author']/text()").get()
        rate = response.xpath("//div[@id='rate']/text()").get()
        yield JobparserItem(url=url, name=name, price_f=price_f, price_s=price_s, author=author, rate=rate)