import pandas as pd


class DataLoader:
    """
    Loads the ICRISAT dataset and caches it in memory.
    """

    def __init__(
        self,
        file_path: str
    ):

        self.file_path = file_path

        self.df = None

    def load(self) -> pd.DataFrame:
        """
        Load dataset only once.
        """

        if self.df is None:

            self.df = pd.read_csv(
                self.file_path
            )

        return self.df

    def get_dataframe(self) -> pd.DataFrame:
        """
        Return loaded dataframe.
        """

        if self.df is None:

            return self.load()

        return self.df

    def get_shape(self):
        """
        Returns dataset shape.
        """

        df = self.get_dataframe()

        return df.shape

    def get_columns(self):
        """
        Returns column names.
        """

        df = self.get_dataframe()

        return df.columns.tolist()

    def dataset_summary(self):
        """
        Useful for debugging.
        """

        df = self.get_dataframe()

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": df.columns.tolist()
        }