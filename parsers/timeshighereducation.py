from urllib.request import urlopen  # Library for urlopen
from bs4 import BeautifulSoup  # Library for html parser (scraper), lxml is also nice
from pathlib import Path
import json
from time import gmtime, strftime
import hashlib

# This folder should be edited according to this project path on yours computer
project_folder = '/home/bogdan/PycharmProjects/universities_sentiment/'
cache_folder = project_folder + 'cache/'
site = 'www.timeshighereducation.com/academic/news/all?page=1'

site_page = Path(cache_folder + site)


def parsing_function(site_tree):
    # Преобразовываем файл к объектному типу библиотеки BeautifulSoup
    site_bs = BeautifulSoup(site_tree, "html.parser")
    # Ищем все вхождения ссылок с главной страницы на статьи
    site_titles = site_bs.find_all('a', class_="article-title")
    for site_title in site_titles:
        article_url = site_title.get('href')
        article_title = site_title.get_text()
        print(article_url)

# Открывайм файл индекса страниц в кэше
with open('../uni_cache/index.json', 'r') as articles_index_file:
    articles_index_data = articles_index_file.read()
    articles_index_json = json.loads(articles_index_data)
    # Пробуем взять название файла страницы, которую хотим парсить, если она не в индексе, выпадет исключение и мы
    # заменим url обратно на site, чтобы скачать страницу из инета
    try:
        url = '../uni_cache/' + articles_index_json[site]
    except KeyError:
        url = site
    # Закрываем файл с индексами
    articles_index_file.close()
    # Теперь проверям (по содержанию строки uni_cache), какой у нас URL: из кэша или обычный, "интернетовский"
    if url.find('uni_cache') != -1:
        print('Using web page from cache...')
        cached_page = open('../uni_cache/' + url, 'r').read()
        parsing_function(cached_page)
    else:
        print('Using web page from internet...')
        # Если страничка не из кэша, то открываем файл с индексами
        articles_index_file = open('../uni_cache/index.json', 'w')
        # Качаем исходники страницы для парсинга
        site_tree = urlopen('http://' + site).read().decode('utf-8', 'ignore')
        # Даём ей название по временной метке и хэшу md5
        parsed_page_name = strftime("%d.%m.%Y-%H", gmtime()) + '-' + hashlib.md5(
            site_tree.encode()).hexdigest() + '.html'
        # Кэшируем страницу в папку с кэшами
        parsed_page = open('../uni_cache/' + parsed_page_name, 'w')
        parsed_page.write(str(site_tree.encode('utf-8')))
        # Добавляем страницу в индекс, т.к. теперь она закэширована
        articles_index_json[url] = parsed_page_name
        json.dump(articles_index_json, articles_index_file, sort_keys=True, indent=4)
        # Парсим то, что загрузили из инета
        parsing_function(site_tree)

