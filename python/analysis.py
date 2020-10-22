import pandas as pd
import sqlite3
from .misc.processing import desc_text, words, word_cloud
from datetime import datetime
from sayn import PythonTask


class NLP(PythonTask):

    def run(self):

        process_start_time = datetime.now()

        logging = self.logger
        user_prefix = self.parameters["user_prefix"]
        table = self.task_parameters["table"]
        database = self.default_db


        # Read from database to dataframe

        df = pd.DataFrame(database.select(f"SELECT * FROM {user_prefix}{table}"))

        # Process the texts from article titles and summaries

        text_fields = self.parameters["text"]

        for t in text_fields:
            logging.info(f"Processing texts for {t} field")
            desc_text(df, t, "english")
            logging.info("Processing Completed!")

        # Load the processed texts back into the database

        df.published = df.published.apply(lambda x: datetime.strptime(x, '%a, %d %b %Y %H:%M:%S %Z')) # Convert published timestamps to datetime

        if df is not None:
            table = user_prefix + "clean_data_nlp"
            n_rows = len(df)
            logging.info(f"Loading {n_rows} rows into destination: {table}....")
            df.to_sql(
                      table,
                      database.engine,
                      if_exists="replace",
                      index=False,
            )
            logging.info("Load done.")


        # Basic text data summaries, grouped by source

        sources = df.groupby("source")

        logging.info("Generating text data summaries grouped by source")

        (sources.title_words.describe()).to_csv("python/summaries/article_title_word_stats.csv")
        logging.info("Generated article_title_word_stats.csv")

        (sources.summary_words.describe()).to_csv("python/summaries/article_summary_word_stats.csv")
        logging.info("Generated article_summary_word_stats.csv")

        # Wordcloud

        logging.info("Prepping word clouds")

        full_text = " ".join(article for article in df.summary)
        grouped_texts = sources.summary.sum()

        stopwords = words()
        stopwords.update(["will", "said","say","says", "US", "Scotland", "England",
                          "Wales", "NI", "Ireland", "Europe","country","BBC", "yn"])

        # Full_text wordcloud

        logging.info("Generating bbc_wordcloud.png")
        word_cloud("bbc", full_text, stopwords, b_colour = "white", c_colour = "black")
        logging.info("bbc_wordcloud.png generated succesfully!")

        # Source specific wordclouds

        for group, text in zip(grouped_texts.keys(), grouped_texts):
            logging.info(f"Generating {group}_wordcloud.png")
            word_cloud(group, text, stopwords)
            logging.info(f"{group}_wordcloud.png generated succesfully!")

        process_end_time = datetime.now()



        # Add process timing to logger

        logging.info("Process done, see details on timing below:")
        logging.info(f"Process started at: {process_start_time}.")
        logging.info(f"Process ended at: {process_end_time}.")

        return self.success()
