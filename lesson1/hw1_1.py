import requests
import json
user = 'brightly'
res1 = requests.get(f'https://api.github.com/users/{user}/repos')
if res1.ok:
    r_data = res1.json()
    print(f'Список отрытых репозиторий для пользователя {user}')
    for i in r_data:
        print(i.get('name'))
with open('data1.json', 'w') as f:
    json.dump(res1.json(), f)
# 2 Задание
# Api по Фильму Властелин колец
# Вывела названия книг и всех героев
url = 'https://the-one-api.dev/v2'
token  = 'KYQF72jL34msocpvTSPS'
my_headers = {
            'Authorization': 'Bearer KYQF72jL34msocpvTSPS'
}
book = '/book'
charac = '/character'
res2 = requests.get(url+book, headers = my_headers)
if res2.ok:
    r2_data = res2.json()
    print(f'List Book:')
    for i in r2_data['docs']:
        print(i.get('name'))

with open('data2.json', 'w') as f:
    json.dump(res2.json(), f)

res3 = requests.get(url+charac, headers = my_headers)
if res2.ok:
    r3_data = res3.json()
    print('List herois:')
    for i in r3_data['docs']:
        print(i.get('name'))

with open('data3.json', 'w') as f:
    json.dump(res3.json(), f)