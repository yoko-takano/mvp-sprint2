import pandas as pd


class DataLoader:

    @staticmethod
    def load_data(url: str, columns: list) -> pd.DataFrame:
        """
        Loads and returns a DataFrame. There are several parameters
        in read_csv that could be used to provide additional options.
        """

        return pd.read_csv(
            url,
            names=columns,
            header=0,
            skiprows=0,
            delimiter=','
        )  # These two parameters are specific to this dataset. You might not need to use them.
