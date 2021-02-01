import pandas as pd
from datetime import datetime
from sayn import PythonTask
from .misc.data_fetch import fetch_data


class LoadData(PythonTask):
    def run(self):

        # Assign the required parameters

        links = self.parameters["links"]
        table = self.parameters["user_prefix"] + self.task_parameters["table"]

        # Declare an empty dataframe

        df = pd.DataFrame()

        # Append data from all links to the empty dataframe

        for link in links:

            temp_df = fetch_data(link)
            n_rows = len(temp_df)
            df = df.append(temp_df)
            self.info(
                f"Loading {n_rows} rows into destination: {table}...."
            )

        # Append the filled dataframe to the database

        if df is not None:
            
            df.to_sql( table
                       ,self.default_db.engine
                       ,if_exists="append"
                       ,index=False)

            self.info("Load done.")


        return self.success()
