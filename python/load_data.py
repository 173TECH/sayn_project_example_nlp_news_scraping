import sqlite3
from .misc.data_fetch import fetch_data
from datetime import datetime
from sayn import PythonTask


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
    def setup(self):
        err = False
        for link in links:
            try:
                self.data_to_load = fetch_data(link)
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

        for link in links:

            table = table_temp + link[29:-8].replace("/","_") # automatic table names

            df = fetch_data(link)
            logging = self.logger
            if df is not None:
                n_rows = len(df)
                logging.info(
                    f"Loading {n_rows} rows into destination: {table}...."
                )
                df.to_sql(
                    table,
                    self.default_db.engine,
                    if_exists="append",
                    index=False,
                )
                logging.info("Load done.")

        process_end_time = datetime.now()

        # print process timing
        logging.info("Process done, see details on timing below:")
        logging.info(
            "Process started at: {process_start_time}.".format(
                process_start_time=process_start_time
            )
        )
        logging.info(
            "Process ended at: {process_end_time}.".format(
                process_end_time=process_end_time
            )
        )

        return self.success()
