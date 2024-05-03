import pandas as pd

from observatoire.tmdb.config import HF_MOVIES_DATASET
from observatoire.tmdb.hf import load_dataset


def load_movies_dataset() -> pd.DataFrame:
    return load_dataset(HF_MOVIES_DATASET)
