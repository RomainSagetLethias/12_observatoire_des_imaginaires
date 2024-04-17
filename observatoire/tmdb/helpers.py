import json
import logging

import pandas as pd


def parse_keywords(keywords: str) -> str:
    """
    Parses the keywords into a list
    """

    keywords_dict = json.loads(keywords)

    keywords_list = []

    for item in keywords_dict["keywords"]:
        keywords_list.append(item["name"])

    return ", ".join(keywords_list)


def merge(df_current: pd.DataFrame | None, df_latest: pd.DataFrame, logger: logging) -> None:
    """
    Merge the current dataset with the new dataset
    """
    logger.info("starting to merge new data with current dataframe")

    df_latest.replace({"Not Available": pd.NA, "1500-01-01": pd.NA, None: pd.NA}, inplace=True)

    # Concatenate the current dataset_df with the new df to merge the data
    merged_df = pd.concat([df_current, df_latest]) if df_current is not None else df_latest
    sorted_df = merged_df.sort_values("vote_count", ascending=False)

    return sorted_df
