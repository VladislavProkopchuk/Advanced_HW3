import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

url = 'https://spb.hh.ru/search/vacancy'
params = {'text': 'python', 'area': 1, 'area': 2}   # 1 - Москва, 2 - Санкт-Петербург

response = requests.get(url, params=params)
vacancies = response.json()

result = []

for vacancy in vacancies['items']:
    if 'Django' in vacancy.get('description', '') and 'Flask' in vacancy.get('description', ''):
        vacancy_info = {'link': vacancy['url'], 'salary': vacancy.get('salary', ''), 'company_name': vacancy['employer']['name'], 'city': vacancy['area']['name'] }
        result.append(vacancy_info)

with open('vacancies.json', 'w') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)