import pandas as pd
from .misc.processing import words, word_cloud
from datetime import datetime
from sayn import PythonTask


class RenderCloud(PythonTask):

    def run(self):

        # Assign the required parameters

        user_prefix = self.parameters["user_prefix"]
        table = self.task_parameters["table"]
        database = self.default_db

        # Read from database to dataframe

        df = pd.DataFrame(database.read_data(f"SELECT * FROM {user_prefix}{table}"))

        self.info("Gathering scattered clouds....")

        # Aggregating texts

        full_text = " ".join(article for article in df.summary)

        # Aggregating texts grouped by source

        sources = df.groupby("source")
        grouped_texts = sources.summary.sum()

        # Getting Stopwords

        stopwords = words()
        stopwords.update(self.parameters["stopwords"])

        # Full_text wordcloud

        self.info("Generating bbc_wordcloud.png")
        word_cloud("bbc", full_text, stopwords, b_colour = "white", c_colour = "black")
        self.info("bbc_wordcloud.png generated succesfully!")

        # Source specific wordclouds

        for group, text in zip(grouped_texts.keys(), grouped_texts):
            self.info(f"Generating {group}_wordcloud.png")
            word_cloud(group, text, stopwords)
            self.info(f"{group}_wordcloud.png generated succesfully!")


        return self.success()
