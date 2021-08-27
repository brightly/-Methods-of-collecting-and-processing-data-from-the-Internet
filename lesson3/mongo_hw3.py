#  https://spb.hh.ru/search/vacancy?schedule=remote&clusters=true&area=2&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=fyfkbnbr
import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pprint import pprint


hh_info = {}
row = 0
url = 'https://spb.hh.ru/search/vacancy'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' 
                         '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

next_p = int(input('Какое количество страниц обработать?'))
vac = input('Какую вакансию ищем?')
max_sal = int(input('Зарплаты выше?'))

client = MongoClient('localhost', 27017)
db = client['MongoGB']
jobs = db.jobs

for i in range(next_p):
    params = {
            'clusters': 'true',
            'enable_snippets':'true',
            'salary': '',
            'st':'searchVacancy',
            'text': vac,
            'page' : i
            }

    response = requests.get(url, params=params, headers=headers)

    soup = bs(response.text, 'html.parser')
    serials = soup.find_all('div', {'class':'vacancy-serp-item'})

    for serial in serials:
        serial_data = {}
        info = serial.find('a',{'data-qa':'vacancy-serp__vacancy-title'})
        name = info.text
        link = info.get('href')
        try:
            salary = serial.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            valuta = salary[salary.rfind(' ') + 1:]
            if salary[:2] == 'от':
                sal_min = int(salary[3:cost.rfind(' ')].replace(u'\u202f',''))
                sal_max = None
            elif salary[:2] == 'до':
                sal_min = None
                sal_max = int(salary[3:cost.rfind(' ')].replace(u'\u202f',''))
            else:
                salary = salary.replace(u'\u202f','')
                sal_min = int(salary[:salary.find(' ')])
                sal_max = int(salary[salary.find(' – ') + 3:salary.rfind(' ')])
        except:
            sal_min = None
            sal_max = None
            valuta = None


        hh_info['name'] = name
        hh_info['link'] = link
        try:
            hh_info['sal_min'] = int(sal_min)
            hh_info['sal_max'] = int(sal_max)
            hh_info['valuta'] = valuta
        except:
            hh_info['sal_min'] = sal_min
            hh_info['sal_max'] = sal_min
            hh_info['valuta'] = valuta

        try:
            if hh_info['sal_min'] >= request_salary_min or job_info['max_salary'] >= request_salary_min:
                pprint(job_info)
                print('\n')
        except:
            pass


        try:
            if hh_info['min_salary'] >= max_sal or hh_info['sal_max'] >= max_sal:
                pprint(hh_info)
                print('\n')
        except:
                pass

        jobs.update_one({'link': hh_info['link']}, {'$set': hh_info}, upsert=True)

f = 0
for i in jobs.find({}):
    f += 1
    pprint(i)
    print(f)