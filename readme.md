# BBC Article Text Analysis




This is a sample SAYN project. It shows you how to implement and use SAYN for data modelling and processing.

For more details, you can see the documentation here: https://173tech.github.io/sayn/


---

**Brief Overview:**

 1. This project scrapes data from the BBC News RSS feeds and writes it into a SQLite database using SAYN's Python Tasks.

 2. Data is cleaned using SAYN's AutoSQL Tasks.

 3. The cleaned data is used for NLP in another Python Task to generate text statistics and wordcloud images.

 ---

 **Project's SAYN process**

 ![Visualisation of this project's SAYN process](/images/dag.png)


----

**Quick Notes:**

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
**Additional Notes:**

- This project has a number of dependencies listed in requirements.txt, to install them please use "pip install -r requirements.txt"
- Visualisation of the whole SAYN process for this project can be found in "images/dag.png"
- Masks for the wordclouds can be found in "python/img/masks"
