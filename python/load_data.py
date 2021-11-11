import pandas as pd
import feedparser as f
from sayn import PythonTask


class LoadData(PythonTask):
    def fetch_reddit_data(self, link):
        """Parse and label RSS Reddit data then return it in a pandas DataFrame"""

        # get data from supplied link

        raw_data = f.parse(link)

        # transform data to dataframe

        data = pd.DataFrame(raw_data.entries)

        # select columns of interest

        data = data.loc[:, ["id", "link", "updated", "published", "title"]]

        # get the source, only works for Reddit RSS feeds

        source_elements = link.split("/")
        data["source"] = source_elements[4] + "_" + source_elements[5]

        return data

    def setup(self):
        self.set_run_steps(["Appending Reddit data to dataframe", "Updating database"])
        return self.success()

    def run(self):

        with self.step("Appending Reddit data to dataframe"):

            links = self.parameters["links"]
            table = self.parameters["user_prefix"] + self.task_parameters["table"]

            df = pd.DataFrame()

            for link in links:

                temp_df = self.fetch_reddit_data(link)
                n_rows = len(temp_df)
                df = df.append(temp_df)
                self.info(f"Loading {n_rows} rows into destination: {table}....")

        with self.step("Updating database"):
            if df is not None:

                df.to_sql(
                    table, self.default_db.engine, if_exists="append", index=False
                )

        return self.success()
