#  https://spb.hh.ru/search/vacancy?schedule=remote&clusters=true&area=2&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=fyfkbnbr
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from pprint import pprint
hh_df = pd.DataFrame(columns = ['hh_id', 'name', 'link', 'sal_min', 'sal_max', 'valuta'])
row = 0
url = 'https://spb.hh.ru/search/vacancy'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' 
                         '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
next_p = int(input('Какое количество страниц обработать?'))
vac = input('Какую вакансию ищем?')
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


        hh_df.loc[row,'name'] = name
        hh_df.loc[row, 'link'] = link
        hh_df.loc[row, 'sal_min'] = sal_min
        hh_df.loc[row, 'sal_max'] = sal_max
        hh_df.loc[row, 'valuta'] = valuta

        row += 1
    hh_df['hh_id'] = hh_df['link'].str.extract('([0-9]{5,})')
print(hh_df)
hh_df.to_csv('out_hh.csv', encoding='utf-8', index=False)