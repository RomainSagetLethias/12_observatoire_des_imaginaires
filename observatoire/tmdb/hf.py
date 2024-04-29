import datasets
import pandas as pd
from datasets import Dataset, DatasetDict


def load_dataset(path: str) -> pd.DataFrame | None:
    try:
        dataset = datasets.load_dataset(
            path,
            split="train",
        )
        dataset.cleanup_cache_files()

        # Load dataset into Pandas DataFrame
        df = dataset.to_pandas()
    except Exception:
        df = None

    return df


def save_dataset(df: pd.DataFrame, path: str) -> None:
    dataset = Dataset.from_pandas(df, preserve_index=False)
    dataset_dict = DatasetDict({"train": dataset})
    dataset_dict.push_to_hub(path)
