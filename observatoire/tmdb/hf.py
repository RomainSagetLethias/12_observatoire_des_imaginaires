import pandas as pd
from datasets import Dataset, DatasetDict, load_dataset


def load_movies_dataset() -> pd.DataFrame | None:
    try:
        data = load_dataset("DataForGood/observatoire_des_imaginaires_movies", split="train")
        # Load dataset into Pandas DataFrame
        df = data.to_pandas()
    except Exception:
        df = None

    return df


def save_movies_dataset(df: pd.DataFrame) -> None:
    dataset = Dataset.from_pandas(df)
    dataset_dict = DatasetDict({"train": dataset})
    dataset_dict.push_to_hub("DataForGood/observatoire_des_imaginaires_movies")
