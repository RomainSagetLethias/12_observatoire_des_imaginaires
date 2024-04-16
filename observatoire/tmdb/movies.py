import concurrent.futures
import contextlib
import json
import logging
import os
import threading
import time
from datetime import UTC, datetime
from http import HTTPStatus
from pathlib import Path

import pandas as pd
import requests
import tqdm

from . import TMDB_API_KEY, TMDB_MAX_RETRIES

# Get current working directory
cwd = Path.cwd()

# Define folder paths
data_folder = Path(cwd) / "TMDB_movie_data"
archive_folder = Path(data_folder) / "TMDB_archive"
output_folder = Path(data_folder) / "temp_movies"
log_file_path = Path(data_folder) / "logs"
saved_movie_tracker_path = Path(archive_folder) / "completed_movie_ids.txt"

# Create necessary folders if they don't exist
Path.mkdir(data_folder, exist_ok=True, parents=True)
Path.mkdir(output_folder, exist_ok=True, parents=True)
Path.mkdir(log_file_path, exist_ok=True, parents=True)
Path.mkdir(archive_folder, exist_ok=True, parents=True)

# Get current date
date_today = datetime.now(UTC).date()
date_today_str = str(date_today)

# Create file path for saving json file
json_save_file_path = Path(archive_folder) / f"{date_today_str}_TMDB_movies.ndjson"

# variable to store the number of movies collected
movies_collected = 0
lock = threading.Lock()
dataset_df = pd.read_csv(
    "site-observable/docs/.observablehq/cache/data/movies.csv",
)
full_log = False  # Mark True to log everything

# Create a logger for the current module


def setup_logger() -> logging:
    # Create a logger for the current module
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Define the log format
    log_formatter = logging.Formatter(
        "%(asctime)s    | %(name)s  | %(levelname)s | %(message)s",
    )

    # Create a stream handler to output log messages to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger


# Get latest movie ID from TMDB API


def get_latest() -> int:
    url = "https://api.themoviedb.org/3/movie/latest"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}",
    }

    # Retry the request until it succeeds
    retries = 0
    while retries < TMDB_MAX_RETRIES:
        try:
            response = requests.get(url, headers=headers)
            break
        except Exception:
            retries += 1
            time.sleep(5)

    # Extract the ID of the latest movie from the response
    response_in_json = json.loads(response.text)
    movies_id = int(response_in_json["id"])

    return movies_id


# Get last movie ID from the saved movie tracker file


def get_oldest() -> int:
    # Get the 'id' value of the last row in the sorted DataFrame
    dataset_df.sort_values(["id"], inplace=True)
    last_id = dataset_df.iloc[-1]["id"]

    return last_id


# Delete old temp files


def delete_old_files(logger: logging) -> None:
    logger.info("Deleting Old temp files")
    try:
        # Get a list of files from the last run in the output folder
        files_from_last_run = os.listdir(output_folder)

        # delete old temp files
        if len(files_from_last_run) > 0:
            for file in files_from_last_run:
                full_file_path = Path(output_folder) / file
                Path.unlink(full_file_path)
    except Exception:
        logger.exception("Error when deleting old temp files")


# Functions the get movie data


def get_keywords(movie_id: int) -> dict | None:
    """
    Gets keywords from TMDB
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == HTTPStatus.OK:
        return response.text
    return None


def parse_keywords(keywords: str) -> str:
    """
    Parses the keywords into a list
    """

    keywords_dict = json.loads(keywords)

    keywords_list = []

    for item in keywords_dict["keywords"]:
        keywords_list.append(item["name"])

    return ", ".join(keywords_list)


def handler_get_keywords(movie_id: int) -> list[int, str]:
    """
    handles getting keywords
    """

    data = get_keywords(movie_id)

    if not data:
        return None

    keywords_str = parse_keywords(data)

    return keywords_str


def process_movie_ids(movie_id: int, logger: logging, pbar: tqdm) -> None:
    global movies_collected  # noqa: PLW0603

    if full_log:
        logger.info(f"Processing {movie_id}")

    # output file path for the current movie
    output_file = Path(output_folder) / f"scrapeTMDB_movies_{movie_id}.ndjson"
    with lock:
        pbar.update(1)

    try:
        time.sleep(0.2)
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_API_KEY}",
        }
        response = requests.get(url, headers=headers)

        if (
            response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR
            or response.status_code == HTTPStatus.TOO_MANY_REQUESTS
        ):
            logger.warning(
                f"movie {movie_id} - Got {response.status_code} response, retrying...",
            )
            time.sleep(1)

        # Process the response if it is successful
        if response.status_code == HTTPStatus.OK:
            rqst_json = response.json()

            keywords = handler_get_keywords(movie_id)
            rqst_json["keywords"] = keywords
            with Path.open(output_file, "a", encoding="utf-8") as append_file:
                append_file.write(json.dumps(rqst_json) + "\n")

            # Increment the count of collected movies and save the movie ID as completed
            # this way, even if the code fails, we can restart where we left off
            # Not needed for daily updates, but if running from 0, this will be userful
            with lock:
                movies_collected += 1
                with Path.open(
                    saved_movie_tracker_path,
                    "a",
                    encoding="utf-8",
                ) as completed_movie_id_file:
                    completed_movie_id_file.write(f"{movie_id}\n")

            if full_log:
                logger.info(f"movies collected: {movies_collected}")

    except Exception:
        logger.exception(f"Expection for {movie_id} in process_movie_ids")

    if full_log:
        logger.info(f"Completed movie {movie_id}")


# Combine threads into one json file


def combine_threads(logger: logging) -> None:
    logger.info("Starting to combine threads")
    thread_dir = output_folder

    count = 0
    file_names = os.listdir(thread_dir)

    # open the save file
    with Path.open(json_save_file_path, "a", encoding="utf-8") as append_file:
        for file in file_names:
            read_file_path = Path(thread_dir) / file
            with Path.open(read_file_path, encoding="utf-8") as read_file:
                for line in read_file:
                    line_data = json.loads(line)
                    count += 1
                    # save the line to the main json
                    append_file.write(f"{json.dumps(line_data)}\n")

    logger.info(f"Finished combining threads. Total movies added: {count}")


# Load json file and make a python list from data


# TODO: load_json_data is too complex and should be refactored
def load_json_data() -> list[dict]:  # noqa: C901, PLR0915
    """
    This function will take the combined thread ndjson file, parse it,
    format it, and return all the movies as python list of dicts
    """

    data = []
    unique_ids = set()

    # load the data
    with Path.open(json_save_file_path, encoding="utf-8") as input_file:
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

        for line in input_file:
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

            formatted_data["id"] = (
                int(line_in_json["id"]) if line_in_json["id"] is not None else 0
            )

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
                if line_in_json["release_date"] is not None
                and line_in_json["release_date"] != ""
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
                float(line_in_json["popularity"])
                if line_in_json["popularity"] is not None
                else 0.0
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


def merger(logger: logging) -> pd.DataFrame:
    logger.info("starting to merge new data with old dataframe")

    # Load and format the json data
    data = load_json_data()

    # Create a DataFrame from the loaded JSON data
    df = pd.DataFrame(data)
    df.replace({"Not Available": pd.NA, "1500-01-01": pd.NA, None: pd.NA}, inplace=True)

    # Concatenate the current dataset_df with the new df to merge the data
    merged_df = pd.concat([dataset_df, df])
    sorted_df = merged_df.sort_values("vote_count", ascending=False)

    return sorted_df


# Executor


def executor() -> pd.DataFrame | None:
    logger = setup_logger()
    logger.info("Starting Executor")

    # first, lets get the id of the lastest movies
    latest = get_latest()

    # second, let's get the last movie from our last run
    oldest = get_oldest()

    # Generate a list of movie IDs
    movie_ids_list = list(range(oldest, latest))
    total_movies_to_process = len(movie_ids_list)

    logger.info(f"Total Movies to Process in this run: {total_movies_to_process}")
    delete_old_files(logger)

    with (
        tqdm(total=total_movies_to_process, unit=" movies") as pbar,
        concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor,
    ):
        futures = []
        for movie in movie_ids_list:
            futures.append(executor.submit(process_movie_ids, movie, logger, pbar))

        for future in concurrent.futures.as_completed(futures):
            with contextlib.suppress(Exception):
                _ = future.result()
    # combine all the threads to one file
    try:
        combine_threads(logger)
    except Exception as error:
        logger.critical(f"Error when combining threads: {error}")
        return None

    # merge today's data with the old dataset
    try:
        df = merger(logger)
    except Exception as error:
        logger.critical(f"Error when merging dataframes {error}")
        return None

    logger.info("Completed Executor")

    return df
