from urllib.request import urlopen  # Library for urlopen
from bs4 import BeautifulSoup  # Library for html parser (scraper), lxml is also nice
from uni_cache.cache_function import cache_function
import pymysql
import collections
import mysql_credits

# This folder should be edited according to this project path on yours computer
project_folder = '/home/bogdan/PycharmProjects/universities_sentiment/'
cache_folder = project_folder + 'cache/'
site = 'www.timeshighereducation.com'


connection = pymysql.connect(
    host=mysql_credits.db_host,
    user=mysql_credits.db_user,
    password=mysql_credits.db_password,
    db=mysql_credits.db_password,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


def parsing_function(site_tree):
    # Преобразовываем файл к объектному типу библиотеки BeautifulSoup
    site_bs = BeautifulSoup(site_tree, "html.parser")
    # Ищем все вхождения ссылок с главной страницы на статьи
    site_titles = site_bs.find_all('a', class_="article-title")
    articles_data = []
    for site_title in site_titles:
        # Создаём что-то вроде ассоциативного массива
        article_meta_data = collections.OrderedDict()
        # Херачим в него ссылки статьи
        article_meta_data['article_url'] = site_title.get('href')
        # Херачим в него заголовки статьи
        article_meta_data['article_title'] = site_title.get_text()
        # Вкорячиваем этот "ассоциативный массив" в просто массив
        articles_data.append(article_meta_data)
    return articles_data





for i in range(1,2):
    site_news_section = '/academic/news/all?page='+str(i)
    site_tree = cache_function(site + site_news_section)
    articles = parsing_function(site_tree)
    # Здесь будем парсить все статьи,собранные с главной страницы
    for article in articles:
        site_tree = cache_function(site + article['article_url'])
        page_article_bs = BeautifulSoup(site_tree, "html.parser")
        page_article = page_article_bs.find_all('div', class_='field-item even')
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `article` (`article_title`, `article_text`, `article_url`, `article_categories`) VALUES (%s, %s, %s, 'null');"
                cursor.execute(sql, (article['article_title'], page_article[1].get_text(), article['article_url']))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        finally:
            print('finally')
connection.close()