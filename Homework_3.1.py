import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

# определяю список ключевых слов
KEYWORDS = ['python', 'Москва', 'Санкт-Петербург', 'Django', 'Flask']
MAIN_LINK = 'https://spb.hh.ru/search/vacancy'

headers = Headers(os='win', headers=True).generate()
ret = requests.get(MAIN_LINK, headers=headers)

soup = BeautifulSoup(ret.text, 'html.parser')
articles = soup.findAll("article", {"class": "tm-articles-list__item"})

article_dicts = []
for article in articles:
	# ищем совпадение по ключевым словам
	hubs = article.findAll("a", {"class": "tm-article-snippet__hubs-item-link"})
	hubs = [hub.span.text.lower() for hub in hubs]
	is_match = False
	matching = [hub for hub in hubs for key in KEYWORDS if key in hub]
	if len(matching):
		is_match = True

	if is_match:
		title = article.find("a", {"class": "tm-article-snippet__title-link"})
		date = article.find("span", {"class":"tm-article-snippet__datetime-published"})
		article_dicts.append({
			"title":title.span.text,
			"ref":MAIN_LINK+title["href"],
			"datetime":date.time["datetime"],
			"matching":matching
			})


for article in article_dicts:
	print(f"{article['datetime']} - {article['title']} - {article['ref']}")
	print(f"matched words: {article['matching']}")
	print()



with open('article_dicts', 'w') as file:
    json.dump(article_dicts, file, ensure_ascii=False, indent=4)


