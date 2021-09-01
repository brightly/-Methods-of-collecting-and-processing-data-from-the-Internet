
from lxml import html
import requests
from datetime import datetime
from pymongo import MongoClient


def get_news_lenta_ru():
    news = []

    keys = ('title', 'date', 'link')
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    link_lenta = 'https://lenta.ru/'

    request = requests.get(link_lenta)

    root = html.fromstring(request.text)
    root.make_links_absolute(link_lenta)

    client = MongoClient('localhost', 27017)
    db = client['MongoGB']
    news_lenta = db.jobs

    news_links = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/@href''')

    news_text = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/text()''')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath('//time[@class="g-date"]/@datetime')
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i], date_format)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)

    for new in news:
        news_lenta.insert(new)

    f = 0
    for i in news_lenta.find({}):
        f += 1
        print(i)
        print(f)

    return

def get_yandex_ru():
    news_ya = []

    keys = ('title', 'date', 'link')
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    link_ya = 'https://yandex.ru/news/'

    request = requests.get(link_ya)

    root = html.fromstring(request.text)
    root.make_links_absolute(link_ya)

    client = MongoClient('localhost', 27017)
    db = client['MongoGB']
    news_y = db.jobs

    news_links = root.xpath('''//a[@class='mg-card__link']/@href''')

    news_text = root.xpath('''//h2[@class='mg-card__title']/text()''')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    # не придумала как сделать с датами поставила текущую
    for i in range(len(news_links)):
        news_date.append(datetime.now())

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'yandex.ru'
        news_ya.append(news_dict)

    for new in news_ya:
        news_y.insert(new)

    f = 0
    for i in news_y.find({}):
        f += 1
        print(i)
        print(f)

    return

get_news_lenta_ru()
get_yandex_ru()