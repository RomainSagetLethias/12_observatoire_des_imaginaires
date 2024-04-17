import concurrent.futures
import contextlib
import json
import logging
import os

import pandas as pd
from tqdm import tqdm

from observatoire.tmdb.hf import load_movies_dataset, save_movies_dataset
from observatoire.tmdb.logging import setup_logger
from observatoire.tmdb.tmdb import get_latest_movie_id, get_movie_data

# variable to store the number of movies collected
movies_collected = 0

full_log = False  # Mark True to log everything


# Functions the get movie data


# TODO: load_json_data is too complex and should be refactored
def load_json_data(movie_json: list[str]) -> list[dict]:  # noqa: C901, PLR0915
    """
    This function will take the combined thread ndjson file, parse it,
    format it, and return all the movies as python list of dicts
    """

    data = []
    unique_ids = set()

    # load the data
    variations_to_ignore = [
        None,
        "",
        "NA",
        "N/A",
        "None",
        "na",
        "n/a",
        "NULL",
        "Not Available",
    ]

    for line in movie_json:
        line_in_json = json.loads(line)

        # TODO: format_list_to_str is too complex and should be refactored
        def format_list_to_str(line_in_json: dict, formatted_data: dict) -> dict:  # noqa: C901, PLR0912
            # convert genres list to str

            genres_str = None
            genres_list = []
            try:
                for genre in line_in_json["genres"]:
                    if genre["name"] is not any(variations_to_ignore):
                        genres_list.append(genre["name"])
                if len(genres_list) > 0:
                    genres_str = ", ".join(genres_list)
            except Exception:
                pass

            formatted_data["genres"] = genres_str

            # convert production_companies list to str
            production_companies_str = None
            production_companies_list = []
            try:
                for company in line_in_json["production_companies"]:
                    if company["name"] is not any(variations_to_ignore):
                        production_companies_list.append(company["name"])
                if len(production_companies_list) > 0:
                    production_companies_str = ", ".join(production_companies_list)
            except Exception:
                pass

            formatted_data["production_companies"] = production_companies_str

            # convert production_countries list to str
            production_countries_str = None
            production_countries_list = []
            try:
                for country in line_in_json["production_countries"]:
                    if country["name"] is not any(variations_to_ignore):
                        production_countries_list.append(country["name"])
                if len(production_countries_list) > 0:
                    production_countries_str = ", ".join(production_countries_list)
            except Exception:
                pass

            formatted_data["production_countries"] = production_countries_str

            # convert spoken_languages list to str
            spoken_languages_str = None
            spoken_languages_list = []
            try:
                for language in line_in_json["spoken_languages"]:
                    if language["english_name"] is not any(variations_to_ignore):
                        spoken_languages_list.append(language["english_name"])
                if len(spoken_languages_list) > 0:
                    spoken_languages_str = ", ".join(spoken_languages_list)
            except Exception:
                pass

            formatted_data["spoken_languages"] = spoken_languages_str

            return formatted_data

        # format the data

        formatted_data = {}

        formatted_data["id"] = int(line_in_json["id"]) if line_in_json["id"] is not None else 0

        formatted_data["title"] = (
            str(line_in_json["title"])
            if line_in_json["title"] is not any(variations_to_ignore)
            else None
        )
        formatted_data["vote_average"] = (
            float(line_in_json["vote_average"])
            if line_in_json["vote_average"] is not None
            else 0.0
        )

        formatted_data["vote_count"] = (
            int(line_in_json["vote_count"]) if line_in_json["vote_count"] is not None else 0
        )

        formatted_data["status"] = (
            str(line_in_json["status"])
            if line_in_json["status"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["release_date"] = (
            str(line_in_json["release_date"])
            if line_in_json["release_date"] is not None and line_in_json["release_date"] != ""
            else "1500-01-01"
        )

        formatted_data["revenue"] = (
            int(line_in_json["revenue"]) if line_in_json["revenue"] is not None else 0
        )

        formatted_data["runtime"] = (
            int(line_in_json["runtime"]) if line_in_json["runtime"] is not None else 0
        )

        formatted_data["adult"] = (
            bool(line_in_json["adult"]) if line_in_json["adult"] is not None else False
        )

        formatted_data["backdrop_path"] = (
            str(line_in_json["backdrop_path"])
            if line_in_json["backdrop_path"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["budget"] = (
            int(line_in_json["budget"]) if line_in_json["budget"] is not None else 0
        )

        formatted_data["homepage"] = (
            str(line_in_json["homepage"])
            if line_in_json["homepage"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["imdb_id"] = (
            str(line_in_json["imdb_id"])
            if line_in_json["imdb_id"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["original_language"] = (
            str(line_in_json["original_language"])
            if line_in_json["original_language"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["original_title"] = (
            str(line_in_json["original_title"])
            if line_in_json["original_title"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["overview"] = (
            str(line_in_json["overview"])
            if line_in_json["overview"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["popularity"] = (
            float(line_in_json["popularity"]) if line_in_json["popularity"] is not None else 0.0
        )

        formatted_data["poster_path"] = (
            str(line_in_json["poster_path"])
            if line_in_json["poster_path"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["tagline"] = (
            str(line_in_json["tagline"])
            if line_in_json["tagline"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["keywords"] = str(line_in_json["keywords"])
        try:
            final_formatted_data = format_list_to_str(line_in_json, formatted_data)
        except Exception:
            continue

        # remove and newline chracters
        updated_data = {}
        for key, value in final_formatted_data.items():
            if isinstance(value, str):  # Check if the value is a string
                updated_value = value.replace("\n", " ").replace("\r", " ")
                updated_data[key] = updated_value
            else:
                updated_data[key] = value

        # add the data to our local list
        if updated_data["id"] not in unique_ids:
            unique_ids.add(updated_data["id"])
            data.append(updated_data)

    return data


# Merge current data with old dataset


def merge(dataset_df: pd.DataFrame | None, df: pd.DataFrame, logger: logging) -> None:
    logger.info("starting to merge new data with old dataframe")

    df.replace({"Not Available": pd.NA, "1500-01-01": pd.NA, None: pd.NA}, inplace=True)

    # Concatenate the current dataset_df with the new df to merge the data
    merged_df = pd.concat([dataset_df, df]) if dataset_df is not None else df
    sorted_df = merged_df.sort_values("vote_count", ascending=False)

    return sorted_df


# Executor


def executor() -> None:
    logger = setup_logger()
    logger.info("Starting Executor")

    # first, lets get the id of the lastest movies
    latest_id = get_latest_movie_id()

    # second, let's get the last movie from our last run
    df_current = load_movies_dataset()
    current_id = df_current["id"].max() if df_current is not None else None

    # Generate a list of movie IDs
    movie_ids_list = list(range(current_id or 1, latest_id))[:10]
    total_movies_to_process = len(movie_ids_list)

    logger.info(f"Total Movies to Process in this run: {total_movies_to_process}")

    with (
        tqdm(total=total_movies_to_process, unit=" movies") as pbar,
        concurrent.futures.ThreadPoolExecutor(
            max_workers=int(os.cpu_count() * 0.8),
        ) as executor,
    ):
        futures = []
        movie_json = []
        for movie in movie_ids_list:
            futures.append(executor.submit(get_movie_data, movie_json, movie, logger, pbar))

        for future in concurrent.futures.as_completed(futures):
            with contextlib.suppress(Exception):
                _ = future.result()

    # merge today's data with the old dataset
    try:
        # Load and format the json data
        data = load_json_data(movie_json)

        # Create a DataFrame from the loaded JSON data
        df = pd.DataFrame(data)

        df_merged = merge(df_current, df, logger)

        # Update the movies dataset on the Hugging Face Hub
        save_movies_dataset(df_merged)
    except Exception as error:
        logger.critical(f"Error when merging dataframes {error}")
        return

    logger.info("Completed Executor")


if __name__ == "__main__":
    executor()
