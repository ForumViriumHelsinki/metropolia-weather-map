import pandas as pd

DATA_CACHE = pd.read_parquet("big_data.parquet")


def load_data_cache():
    print("Cache loading")
    # pylint: disable=global-statement
    global DATA_CACHE
    DATA_CACHE = pd.read_parquet("big_data.parquet")
    print("Cache updated")
