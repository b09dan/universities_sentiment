SELECT DISTINCT(article_text), article_uni, article_url, article_rating
FROM article
WHERE article_rating != 0
AND article_text != ''
AND article_text !='no_review_text'