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


def parsing_function(url):
    site_tree = urlopen(url).read().decode('utf-8', 'ignore')  # Making url, reading web-page and converting it to utf-8
    site_bs = BeautifulSoup(site_tree, "html.parser")  # Converting to BS type
    site_titles = site_bs.find_all('a', class_="article-title")  # finding all pics with news link
    # articles_links = []
    i = 0
    for site_title in site_titles:
        article_url = site_title.get('href')
        article_title = site_title.get_text()
        print(article_title)

#
with open('../uni_cache/index.json', 'r') as articles_index_file:
    articles_index_data = articles_index_file.read()
    articles_index_json = json.loads(articles_index_data)
    try:
        url = '../uni_cache/' + articles_index_json[site]
    except KeyError:
        url = site
    print(url)
    articles_index_file.close()
    if url.find('uni_cache') != -1:
        print('yes')
        print(url.find('uni_cache'))
    else:
        articles_index_file = open('../uni_cache/index.json', 'w')
        site_tree = urlopen('http://'+site).read().decode('utf-8', 'ignore')
        parsed_page_name = strftime("%d.%m.%Y-%H", gmtime())+'-'+hashlib.md5(site_tree.encode()).hexdigest()
        articles_index_json[url]=parsed_page_name
        parsed_page = open('../uni_cache/'+parsed_page_name, 'w')
        parsed_page.write(site_tree)
        json.dump(articles_index_json, articles_index_file, sort_keys=True, indent=4)
        #parsing_function(url)
        # articles_index_file.write(str(articles_index_json))

        # if site_page.is_file():
        #     parsing_function(site_page)
        # else:
        #     parsing_function('http://'+site)
        #     site_page_file = open(site_page)
        #     site_page_file.write(urlopen('http://'+site).read().decode('utf-8', 'ignore'))
        #     site_page_file.close()
