SELECT source
     , AVG(title_letters)
     , AVG(title_words)
     , AVG(title_sentences)
     , AVG(summary_letters)
     , AVG(summary_words)
     , AVG(summary_sentences)

FROM {{user_prefix}}{{table}}

GROUP BY 1

ORDER BY 1
