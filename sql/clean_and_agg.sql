SELECT DISTINCT(id)
     , "england" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}england

UNION

SELECT DISTINCT(id)
     , "northern_ireland" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}northern_ireland

UNION

SELECT DISTINCT(id)
     , "scotland" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}scotland

UNION

SELECT DISTINCT(id)
     , "wales" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}wales

UNION

SELECT DISTINCT(id)
     , "africa" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}world_africa

UNION

SELECT DISTINCT(id)
     , "asia" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}world_asia

UNION

SELECT DISTINCT(id)
     , "europe" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}world_europe

UNION

SELECT DISTINCT(id)
     , "latin_america" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}world_latin_america

UNION

SELECT DISTINCT(id)
     , "middle_east" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}world_middle_east

UNION

SELECT DISTINCT(id)
     , "us_and_canada" AS source
     , title
     , summary
     , link
     , guidislink
     , published
FROM {{user_prefix}}{{table}}world_us_and_canada
