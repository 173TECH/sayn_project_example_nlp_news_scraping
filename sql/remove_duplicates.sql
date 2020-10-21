SELECT DISTINCT(id)
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}
