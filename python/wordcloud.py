import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sayn import PythonTask
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


class RenderCloud(PythonTask):
    def word_cloud(
        self, name, text, stopwords, b_colour="white", c_colour="black", show=False
    ):
        """Word cloud generating function"""

        # attempt to find a compatible mask

        try:
            mask = np.array(Image.open(f"python/img/masks/{name}_mask.png"))
            image_colours = ImageColorGenerator(mask)
        except:
            mask = None
            image_colours = None

        wordcloud = WordCloud(
            stopwords=stopwords,
            max_words=100,
            mask=mask,
            background_color=b_colour,
            contour_width=1,
            contour_color=c_colour,
            color_func=image_colours,
        ).generate(text)

        # store wordcloud image in "python/img"

        wordcloud.to_file(f"python/img/{name}_wordcloud.png")

        # declare show=True if you want to show wordclouds

        if show:
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.show()

    def setup(self):
        self.set_run_steps(["Grouping texts", "Generating clouds"])
        return self.success()

    def run(self):

        with self.step("Grouping texts"):

            table = self.parameters["user_prefix"] + self.task_parameters["table"]

            df = pd.DataFrame(self.default_db.read_data(f"SELECT * FROM {table}"))
            full_text = " ".join(article for article in df.title)

            sources = df.groupby("source")
            grouped_texts = sources.title.sum()

        with self.step("Generating clouds"):

            stopwords = STOPWORDS.update(self.parameters["stopwords"])
            self.info("Generating reddit_wordcloud.png")
            self.word_cloud("reddit", full_text, stopwords)

            # Source specific wordclouds

            for group, text in zip(grouped_texts.keys(), grouped_texts):
                self.info(f"Generating {group}_wordcloud.png")
                self.word_cloud(
                    group, text, stopwords, b_colour="black", c_colour="white"
                )

        return self.success()
