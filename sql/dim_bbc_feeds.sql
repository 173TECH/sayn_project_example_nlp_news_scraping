SELECT DISTINCT unique_id
     , id
     , title
     , summary
     , link
     , guidislink
     , published
     , source

FROM {{user_prefix}}logs_bbc_feeds
