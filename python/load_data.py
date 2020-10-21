import pandas as pd
from datetime import datetime
from sayn import PythonTask
from .misc.data_fetch import fetch_data


links = ["http://feeds.bbci.co.uk/news/england/rss.xml",
         "http://feeds.bbci.co.uk/news/wales/rss.xml",
         "http://feeds.bbci.co.uk/news/scotland/rss.xml",
         "http://feeds.bbci.co.uk/news/northern_ireland/rss.xml",
         "http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
         "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
         "http://feeds.bbci.co.uk/news/world/latin_america/rss.xml",
         "http://feeds.bbci.co.uk/news/world/europe/rss.xml",
         "http://feeds.bbci.co.uk/news/world/asia/rss.xml",
         "http://feeds.bbci.co.uk/news/world/africa/rss.xml"]


class LoadData(PythonTask):
    def run(self):

        process_start_time = datetime.now()

        table = self.parameters["user_prefix"] + self.parameters["temp_table"]
        logging = self.logger

        df = pd.DataFrame()

        for link in links:

            temp_df = fetch_data(link)
            n_rows = len(temp_df)
            df = df.append(temp_df)
            logging.info(
                f"Loading {n_rows} rows into destination: {table}...."
            )
        if df is not None:
            df.to_sql( table
                       ,self.default_db.engine
                       ,if_exists="append"
                       ,index=False,
            )
            logging.info("Load done.")

        process_end_time = datetime.now()

        # Add process timing to logger

        logging.info("Process done, see details on timing below:")
        logging.info(f"Process started at: {process_start_time}.")
        logging.info(f"Process ended at: {process_end_time}.")

        return self.success()
