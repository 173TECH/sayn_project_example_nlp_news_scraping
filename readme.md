# Reddit Article Text Analysis

This is a sample SAYN project. It shows you how to implement and use SAYN for data modelling and processing.

For more details, you can see the documentation here: https://173tech.github.io/sayn/


## Project Description

 1. This project scrapes data from the Reddit News RSS feeds and writes it into a SQLite database using SAYN's Python Tasks.

 2. Data is cleaned using SAYN's AutoSQL Tasks.

 3. The cleaned data is used for NLP in another Python Task to generate text statistics and wordcloud images.

 To run the project, you will need to:

 - clone the repository with `git clone https://github.com/173TECH/sayn_project_example_nlp_news_scraping.git`.
 - rename the `sample_settings.yaml` file to `settings.yaml`.
 - install the project dependencies by running the `pip install -r requirements.txt` command from the root of the project folder.
 - use `sayn run` from the root of the project folder to run all SAYN commands.

 After a successful run you should see 4 new files in `python/img`, these should be the following:

 - EUnews_new_wordcloud.png
 - UKnews_new_wordcloud.png
 - USnews_new_wordcloud.png
 - reddit_wordcloud.png

---

## Project's SAYN process

 ![Visualisation of this project's SAYN process](/images/dag.png)


----

## Quick Notes

SAYN uses 2 key files to control the project:

  - settings.yaml: individual settings which are not shared **(Note: You will need to rename the file `sample_settings.yaml` to `settings.yaml` before using "sayn run")**
  - project.yaml: project settings which are shared across all collaborators on the project

**Tip: You can set your user_prefix in the `settings.yaml` file, it can be found in the profiles section under parameters**

SAYN code is stored in 3 main folders:

  - tasks: where the SAYN tasks are defined
  - sql: for SQL tasks
  - python: for python tasks

SAYN uses some key commands for run:

  - sayn run: run the whole project
    - -p flag to specify a profile when running sayn: e.g. sayn run -p prod
    - -t flag to specify tasks to run: e.g. sayn run -t task_name
    - -t group:group_name to specify a group of tasks to run from the tasks folder: e.g. sayn run -t group:group_name
  - sayn compile: compiles the code (similar flags apply)
  - sayn --help for full detail on commands

---
## Additional Notes:

- Visualisation of the whole SAYN process for this project can be found in "images/dag.png"
- Masks for the wordclouds can be found in "python/img/masks"
