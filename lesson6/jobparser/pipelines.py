# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books0809


    def process_item(self, item, spider):
        item['price_s'] = self.price_sale(item['price_f'], item['price_s'])
        item['price_f'] = self.pr_int(item['price_f'])
        item['rate'] = self.pr_float(item['rate'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def price_sale(self, full, sale):
        return int(full) - int(sale)

    def pr_int(self, pref):
        return int(pref)

    def pr_float(self,rate):
        return float(rate)

