import pandas as pd
from .misc.processing import desc_text
from datetime import datetime
from sayn import PythonTask


class NLP(PythonTask):

    def run(self):

        process_start_time = datetime.now()

        user_prefix = self.parameters["user_prefix"]
        table = self.task_parameters["table"]
        text_fields = self.parameters["text"]

        logging = self.logger
        database = self.default_db


        # Read from database to dataframe

        df = pd.DataFrame(database.select(f"SELECT * FROM {user_prefix}{table}"))

        # Process the texts from article titles and summaries

        for t in text_fields:
            logging.info(f"Processing texts for {t} field")
            desc_text(df, t, "english")
            logging.info("Processing Completed!")

        # Load the processed texts back into the database

        df.published = df.published.apply(lambda x: datetime.strptime(x, '%a, %d %b %Y %H:%M:%S %Z')) # Convert published timestamps to datetime

        if df is not None:
            output = f"{user_prefix}{table}_{self.name}"
            n_rows = len(df)
            logging.info(f"Loading {n_rows} rows into destination: {output}....")
            df.to_sql(
                      output,
                      database.engine,
                      if_exists="replace",
                      index=False,
            )
            logging.info("Load done.")

        process_end_time = datetime.now()

        # Add process timing to logger

        logging.info("Process done, see details on timing below:")
        logging.info(f"Process started at: {process_start_time}.")
        logging.info(f"Process ended at: {process_end_time}.")

        return self.success()
