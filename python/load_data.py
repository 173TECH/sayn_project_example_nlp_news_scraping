import pandas as pd
import feedparser as f
from sayn import PythonTask


class LoadData(PythonTask):
    def fetch_bbc_data(self, link):
        """Parse and label RSS BBC News data then return it in a pandas DataFrame"""

        # get data from supplied link

        raw_data = f.parse(link)

        # transform data to dataframe

        data = pd.DataFrame(raw_data.entries)

        # remove incompatible columns

        data.drop(
            ["title_detail", "summary_detail", "links", "published_parsed"],
            axis=1,
            inplace=True,
        )

        # get the source (this only works for BBC RSS feeds)

        data["source"] = link[29:-8].replace("/", "_")

        # generating ids to be unique, since same story ids can be published in different sources

        data["unique_id"] = data["id"] + data["source"]

        return data

    def setup(self):
        self.set_run_steps(["Appending BBC data to dataframe", "Updating database"])
        return self.success()

    def run(self):

        with self.step("Appending BBC data to dataframe"):

            links = self.parameters["links"]
            table = self.parameters["user_prefix"] + self.task_parameters["table"]

            df = pd.DataFrame()

            for link in links:

                temp_df = self.fetch_bbc_data(link)
                n_rows = len(temp_df)
                df = df.append(temp_df)
                self.info(f"Loading {n_rows} rows into destination: {table}....")

        with self.step("Updating database"):
            if df is not None:

                df.to_sql(
                    table, self.default_db.engine, if_exists="append", index=False
                )

        return self.success()
