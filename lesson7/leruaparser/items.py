# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_price(value):
    value = value.replase(' ', '')
    try:
        return int(value)
    except:
        return value

def process_price_dr(value):
    value = value.replase(' ', '')
    try:
        return float(value)
    except:
        return value
def process_list(value_list):
    for lst in value_list:
        lst = lst.replase(' ', '')
        lst = lst.replase('/n', '')
        try:
            return value_list
        except:
            return value_list

class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor= MapCompose(process_price),output_processor=TakeFirst())
    price_dr = scrapy.Field(input_processor= MapCompose(process_price_dr),output_processor=TakeFirst())
    photos = scrapy.Field()
    list_hkt = scrapy.Field(input_processor= MapCompose(process_list))
    list_data_har = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
