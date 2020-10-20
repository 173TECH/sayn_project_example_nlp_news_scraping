import pandas as pd
import sqlite3
from .misc.processing import desc_text, words, word_cloud
from datetime import datetime
from sayn import PythonTask


class NLP(PythonTask):
    def setup(self):
        err = False
        try:
            # Connect and read from database
            conn = sqlite3.connect("dev.db")
            self.data = pd.read_sql_query("select * from ts_full_cleaned_data;", conn)
        except Exception as e:
            err = True
            self.logger.error(e)

        if err:
            return self.failed()
        else:
            return self.ready()

    def run(self):

        process_start_time = datetime.now()

        table_temp = self.project_parameters["user_prefix"] + self.project_parameters["table"]

        # Process the texts from article titles and summaries
        text_fields = ["title", "summary"]

        for t in text_fields:
            self.logger.info(f"Processing texts for {t} field")
            desc_text(self.data, t, "english")
            self.logger.info("Processing Completed!")

        # Basic text data summaries, grouped by source

        sources = self.data.groupby("source")

        print("\n Article Title Word Stats \n")
        print(sources.title_words.describe())
        (sources.title_words.describe()).to_csv("article title word stats.csv")
        print("\n Article Summary Word Stats \n")
        print(sources.summary_words.describe())
        (sources.summary_words.describe()).to_csv("article summary word stats.csv")
        grouped_texts = sources.summary.sum()

        full_text = " ".join(article for article in self.data.summary)
        stopwords = words()
        stopwords.update(["will", "said","say","says", "US", "Scotland", "England", "Wales", "NI", "Ireland", "Europe","country","BBC", "yn"])

        word_cloud("bbc", full_text, stopwords)

        for group, text in zip(grouped_texts.keys(), grouped_texts):
            word_cloud(group, text, stopwords)
