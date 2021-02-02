import pandas as pd
from .misc.processing import desc_text
from sayn import PythonTask


class LanguageProcessing(PythonTask):
    def setup(self):
        self.set_run_steps(
            [
                "Assigning required parameters",
                "Processing texts",
                "Updating database"
            ]
        )
        return self.success()

    def run(self):

        with self.step("Assigning required parameters"):
            table = self.parameters["user_prefix"] + self.task_parameters["table"]
            text_fields = self.parameters["text"]


        with self.step("Processing texts"):

            df = pd.DataFrame(self.default_db.read_data(f"SELECT * FROM {table}"))

            for t in text_fields:
                self.info(f"Processing texts for {t} field")
                desc_text(df, t, "english")
                self.info("Processing Completed!")


        with self.step("Updating database"):
            if df is not None:
                output = f"{table}_{self.name}"
                n_rows = len(df)
                self.info(f"Loading {n_rows} rows into destination: {output}....")
                df.to_sql( output,
                           self.default_db.engine,
                           if_exists="replace",
                           index=False)
                self.info("Load done.")


        return self.success()
