import pandas as pd
from .misc.processing import words, word_cloud
from sayn import PythonTask


class RenderCloud(PythonTask):
    def setup(self):
        self.set_run_steps(
            [
                "Assigning required parameters",
                "Aggregating texts",
                "Getting stopwords",
                "Generating clouds"
            ]
        )
        return self.success()


    def run(self):

        with self.step("Assigning required parameters"):
            table = self.parameters["user_prefix"] + self.task_parameters["table"]


        with self.step("Aggregating texts"):

            df = pd.DataFrame(self.default_db.read_data(f"SELECT * FROM {table}"))
            full_text = " ".join(article for article in df.summary)

            sources = df.groupby("source")
            grouped_texts = sources.summary.sum()


        with self.step("Getting stopwords"):

            stopwords = words()
            stopwords.update(self.parameters["stopwords"])


        with self.step("Generating clouds"):

            self.info("Generating bbc_wordcloud.png")
            word_cloud("bbc", full_text, stopwords, b_colour = "white", c_colour = "black")
            self.info("bbc_wordcloud.png generated succesfully!")

            # Source specific wordclouds

            for group, text in zip(grouped_texts.keys(), grouped_texts):
                self.info(f"Generating {group}_wordcloud.png")
                word_cloud(group, text, stopwords)
                self.info(f"{group}_wordcloud.png generated succesfully!")


        return self.success()
