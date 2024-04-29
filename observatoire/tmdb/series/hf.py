import pandas as pd

from observatoire.tmdb.config import HF_SERIES_DATASET
from observatoire.tmdb.hf import load_dataset


def load_series_dataset() -> pd.DataFrame:
    return load_dataset(HF_SERIES_DATASET)
