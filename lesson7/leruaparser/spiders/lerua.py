import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader
class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query,**kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response:HtmlResponse):
        print()
        ads_links = response.xpath("//a[@data-qa='product-name']")
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in ads_links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()" )
        loader.add_xpath('price_dr', "//span[@slot='fract']/text()")
        loader.add_xpath('photos', '//uc-pdp-media-carousel/picture/img/@src')
        loader.add_xpath('list_hkt','//dt[@class="def-list__term"]/text()')
        loader.add_xpath('list_data_har', '//dd[@class="def-list__definition"]/text()')
        loader.add_value('url', response.url)
        print()
        yield loader.load_item()
        #name = response.xpath("//h1/text()").get()
        #price = response.xpath("//span[@slot='price']/text()").get()
        #price_dr = response.xpath("//span[@slot='fract']/text()").get()
        #photos = response.xpath('//uc-pdp-media-carousel/picture/img/@src').getall()
        #list_hkt = response.xpath('//dt[@class="def-list__term"]/text()').getall()
        #list_data_har = response.xpath('//dd[@class="def-list__definition"]/text()').getall()
        #yield LeruaparserItem(name = name, price=price, price_dr=price_dr, photos=photos, list_hkt= list_hkt, list_data_har=list_data_har)
