import logging

import pandas as pd


def merge(df_current: pd.DataFrame | None, df_latest: pd.DataFrame, logger: logging) -> None:
    """
    Merge the current dataset with the new dataset
    """
    logger.info("starting to merge new data with current dataframe")

    df_latest.replace({"Not Available": pd.NA, "1500-01-01": pd.NA, None: pd.NA}, inplace=True)

    # Concatenate the current dataset_df with the new df to merge the data
    merged_df = pd.concat([df_current, df_latest]) if df_current is not None else df_latest
    merged_df.reset_index(drop=True, inplace=True)

    # sort by id column
    merged_df.sort_values(by="id", inplace=True)

    # Drop unnecessary columns
    merged_df = merged_df.drop(
        columns=[col for col in merged_df.columns if col.startswith("__")],
    )

    return merged_df
