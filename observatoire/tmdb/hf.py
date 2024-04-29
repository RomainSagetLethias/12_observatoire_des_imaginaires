import pandas as pd
from datasets import Dataset, DatasetDict, load_dataset


def load_movies_dataset(path: str) -> pd.DataFrame | None:
    try:
        dataset = load_dataset(
            path,
            split="train",
        )
        dataset.cleanup_cache_files()

        # Load dataset into Pandas DataFrame
        df = dataset.to_pandas()
    except Exception:
        df = None

    return df


def save_movies_dataset(df: pd.DataFrame, path: str) -> None:
    dataset = Dataset.from_pandas(df, preserve_index=False)
    dataset_dict = DatasetDict({"train": dataset})
    dataset_dict.push_to_hub(path)
