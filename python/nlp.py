### Uncomment the block below if you do not have punkt installed, you only need to run this once ###
# import nltk
# nltk.download('punkt')

import pandas as pd
from sayn import PythonTask
from nltk.tokenize import word_tokenize, sent_tokenize


class LanguageProcessing(PythonTask):

    def desc_text(self, df, text_field, language):
        """Text stats generating function"""

        # counts the number of letters in text_field

        df[text_field + "_letters"] = df[text_field].fillna("").str.len()

        # counts the number of words in text_field

        df[text_field + "_words"] = df[text_field].fillna("").apply(lambda x: len(word_tokenize(x, language=language)))

        # counts the number of sentences in text_field

        df[text_field +"_sentences"] = df[text_field].fillna("").apply(lambda x: len(sent_tokenize(x, language=language)))


    def setup(self):
        self.set_run_steps(
            [
                "Processing texts",
                "Updating database"
            ]
        )
        return self.success()


    def run(self):

        with self.step("Processing texts"):

            table = self.parameters["user_prefix"] + self.task_parameters["table"]
            text_fields = self.parameters["text"]

            df = pd.DataFrame(self.default_db.read_data(f"SELECT * FROM {table}"))

            for t in text_fields:
                self.info(f"Processing texts for {t} field")
                self.desc_text(df, t, "english")


        with self.step("Updating database"):
            if df is not None:

                output = f"{table}_{self.name}"
                n_rows = len(df)
                self.info(f"Loading {n_rows} rows into destination: {output}....")
                df.to_sql( output,
                           self.default_db.engine,
                           if_exists="replace",
                           index=False)


        return self.success()
