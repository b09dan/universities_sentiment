from urllib.request import urlopen  # Library for urlopen
from bs4 import BeautifulSoup  # Library for html parser (scraper), lxml is also nice
from uni_cache.cache_function import cache_function
import pymysql
import collections
import mysql_credits


site = 'https://www.studentcrowd.com/university-l1001651-s1008235-university_of_exeter-exeter'
uni_name = 'University of Exeter'

connection = pymysql.connect(
    host=mysql_credits.db_host,
    user=mysql_credits.db_user,
    password=mysql_credits.db_password,
    db=mysql_credits.db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)



def parsing_function(site_tree):
    # Преобразовываем файл к объектному типу библиотеки BeautifulSoup
    site_bs = BeautifulSoup(site_tree, "html.parser")
    # Ищем все вхождения ссылок с главной страницы на статьи
    site_reviews = site_bs.find_all("div", attrs={"itemprop": "review"})
    articles_data = []
    for site_review in site_reviews:
        # Создаём что-то вроде ассоциативного массива
        article_meta_data = collections.OrderedDict()
        # Херачим в него текст отзывов
        if site_review.find("span", attrs={"itemprop": "reviewBody"}):
            article_meta_data['review_text'] = site_review.find("span", attrs={"itemprop": "reviewBody"}).get_text()
        else:
            article_meta_data['review_text'] = 'no_review_text'
        # Херачим в него рейтинг отзыва
        article_meta_data['review_stars'] = int(site_review.find('div', class_="review-box__stars").attrs['class'][2].replace('stars--lg--', ''))
        # Херачим в него дату отзыва
        article_meta_data['review_date'] = site_review.find("meta", attrs={"itemprop": "datePublished"}).attrs['content']
        # Вкорячиваем этот "ассоциативный массив" в просто массив
        articles_data.append(article_meta_data)
    return articles_data

oxford_tree = cache_function(site)
oxford_reviews = parsing_function(oxford_tree)


for oxford_review in oxford_reviews:
    try:
        with connection.cursor() as cursor:
            # Create a new record
            # sql = "INSERT INTO `article` (`article_pub_date`, `article_title`, `article_text`, `article_url`, `article_rating`, `article_uni`, `uni_site_id`, `article_categories`) VALUES (%s, %s, %s, %s, %s, $s, 2, 'null');"
            # cursor.execute(sql, (oxford_review['review_date'], 'no_title', oxford_review['review_text'], 'no_url', oxford_review['review_stars'], uni_name))
            sql = "INSERT INTO `article` (`article_pub_date`, `article_title`, `article_text`, `article_url`, `article_rating`, `article_uni`, `uni_site_id`) VALUES ('"+oxford_review['review_date']+"', 'no_title', '"+oxford_review['review_text'].replace("'","")+"', '"+site+"', "+str(oxford_review['review_stars'])+", '"+uni_name+"', 2);"
            cursor.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        print('Done!')
connection.close()