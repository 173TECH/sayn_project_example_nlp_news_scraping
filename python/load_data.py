import pandas as pd
from sayn import PythonTask
from .misc.data_fetch import fetch_data


class LoadData(PythonTask):
    def setup(self):
        self.set_run_steps(
            [
                "Assigning required parameters",
                "Appending data to dataframe",
                "Updating database"
            ]
        )
        return self.success()


    def run(self):

        with self.step("Assigning required parameters"):
            links = self.parameters["links"]
            table = self.parameters["user_prefix"] + self.task_parameters["table"]


        with self.step("Appending data to dataframe"):

            df = pd.DataFrame()

            for link in links:

                temp_df = fetch_data(link)
                n_rows = len(temp_df)
                df = df.append(temp_df)
                self.info(
                    f"Loading {n_rows} rows into destination: {table}...."
                )


        with self.step("Updating database"):
            if df is not None:

                df.to_sql( table
                           ,self.default_db.engine
                           ,if_exists="append"
                           ,index=False)

                self.info("Load done.")


        return self.success()
