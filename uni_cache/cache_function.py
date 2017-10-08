from pathlib import Path
import json
from time import gmtime, strftime
import hashlib
from urllib.request import urlopen
from urllib.request import Request, urlopen


def cache_function(site_url):
    # Открывайм файл индекса страниц в кэше
    with open('../uni_cache/index.json', 'r') as articles_index_file:
        articles_index_data = articles_index_file.read()
        articles_index_json = json.loads(articles_index_data)
        # Пробуем взять название файла страницы, которую хотим парсить, если она не в индексе, выпадет исключение и мы
        # заменим url обратно на site, чтобы скачать страницу из инета
        try:
            url = '../uni_cache/' + articles_index_json[site_url]
        except KeyError:
            url = site_url
        # Закрываем файл с индексами
        articles_index_file.close()
        # Теперь проверям (по содержанию строки uni_cache), какой у нас URL: из кэша или обычный, "интернетовский"
        if url.find('uni_cache') != -1:
            print('Using web page from cache...')
            cached_page = open('../uni_cache/' + url, 'r').read()
            # articles_urls = parsing_function(cached_page)
            return cached_page
        else:
            print('Using web page from internet...')
            # Если страничка не из кэша, то открываем файл с индексами
            articles_index_file = open('../uni_cache/index.json', 'w')
            # Прикидываемся файерфоксом
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site_url, headers=hdr)
            # Качаем исходники страницы для парсинга
            site_tree = urlopen(req).read().decode('utf-8', 'ignore')
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
            # articles_urls = parsing_function(site_tree)
            return site_tree