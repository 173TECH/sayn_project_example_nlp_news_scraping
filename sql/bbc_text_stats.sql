SELECT source
     , AVG(title_letters) AS average_tl
     , AVG(title_words) AS average_tw
     , AVG(title_sentences) AS average_ts
     , AVG(summary_letters) AS average_sl
     , AVG(summary_words) AS average_sw
     , AVG(summary_sentences) AS average_sss

FROM {{user_prefix}}f_bbc_feeds_nlp

GROUP BY 1

ORDER BY 1
