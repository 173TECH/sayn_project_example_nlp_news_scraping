SELECT source
     , AVG(title_letters) AS average_letters
     , AVG(title_words) AS average_words
     , AVG(title_sentences) AS average_sentences

FROM {{user_prefix}}dim_reddit_feeds_nlp

GROUP BY 1

ORDER BY 1
