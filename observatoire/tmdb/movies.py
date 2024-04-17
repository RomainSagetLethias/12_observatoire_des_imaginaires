import concurrent.futures
import contextlib
import os

from tqdm import tqdm

from observatoire.tmdb.data import transform_movie_json
from observatoire.tmdb.helpers import merge
from observatoire.tmdb.hf import load_movies_dataset, save_movies_dataset
from observatoire.tmdb.logging import setup_logger
from observatoire.tmdb.tmdb import get_latest_movie_id, get_movie_data


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
        df_latest = transform_movie_json(movie_json)

        df_merged = merge(df_current, df_latest, logger)

        # Update the movies dataset on the Hugging Face Hub
        save_movies_dataset(df_merged)
    except Exception as error:
        logger.critical(f"Error when merging dataframes {error}")
        return

    logger.info("Completed Executor")


if __name__ == "__main__":
    executor()
