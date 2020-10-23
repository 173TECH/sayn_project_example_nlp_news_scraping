import pandas as pd
from .misc.processing import words, word_cloud
from datetime import datetime
from sayn import PythonTask


class RenderCloud(PythonTask):

    def run(self):


        process_start_time = datetime.now()


        user_prefix = self.parameters["user_prefix"]
        table = self.task_parameters["table"]

        logging = self.logger

        # Read from database to dataframe

        df = pd.DataFrame(self.default_db.select(f"SELECT * FROM {user_prefix}{table}"))

        logging.info("Gathering scattered clouds....")

        # Aggregating texts

        full_text = " ".join(article for article in df.summary)

        # Aggregating texts grouped by source

        sources = df.groupby("source")
        grouped_texts = sources.summary.sum()

        # Getting Stopwords

        stopwords = words()
        stopwords.update(self.parameters["stopwords"])

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
