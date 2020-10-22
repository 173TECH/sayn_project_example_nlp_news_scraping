SELECT DISTINCT(id)
     , title
     , summary
     , link
     , guidislink
     , published
     , source
FROM {{user_prefix}}{{table}}
