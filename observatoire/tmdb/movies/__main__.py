import concurrent.futures
import contextlib
import os

from tqdm import tqdm

from observatoire.tmdb.config import HF_MOVIES_DATASET, TMDB_BATCH_SIZE
from observatoire.tmdb.helpers import merge
from observatoire.tmdb.hf import load_dataset, save_dataset
from observatoire.tmdb.logger import setup_logger
from observatoire.tmdb.movies.data import make_movie_df
from observatoire.tmdb.movies.tmdb import get_latest_movie_id, get_movie_data


def executor() -> None:
    logger = setup_logger()
    logger.info("Starting Executor")

    # first, lets get the id of the lastest movies
    latest_id = get_latest_movie_id()

    # second, let's get the last movie from our last run
    df_current = load_dataset(HF_MOVIES_DATASET)
    current_id = df_current["id"].max() if df_current is not None else None

    # Generate a list of movie IDs
    movie_ids_list = list(range(current_id or 1, latest_id))
    total_movies_to_process = len(movie_ids_list)

    logger.info(f"Total Movies to Process in this run: {total_movies_to_process}")

    # Split movie_ids_list into chunks of TMDB_BATCH_SIZE
    batches = [
        movie_ids_list[i : i + TMDB_BATCH_SIZE]
        for i in range(0, len(movie_ids_list), TMDB_BATCH_SIZE)
    ]

    with tqdm(total=total_movies_to_process, unit=" movies") as pbar:
        for batch in batches:
            logger.info(f"Processing batch of {len(batch)} movies")

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=int(os.cpu_count() * 0.8),
            ) as executor:
                futures = []
                movie_json = []
                for movie in batch:
                    futures.append(
                        executor.submit(get_movie_data, movie_json, movie, logger, pbar),
                    )

                for future in concurrent.futures.as_completed(futures):
                    with contextlib.suppress(Exception):
                        _ = future.result()

            # merge today's data with the old dataset
            try:
                # Load and format the json data
                df_latest = make_movie_df(movie_json)

                df_merged = merge(df_current, df_latest, logger)

                # Update the movies dataset on the Hugging Face Hub
                logger.info("Will update dataset on Hugging Face Hub")
                save_dataset(df_merged, HF_MOVIES_DATASET)

            except Exception as error:
                logger.critical(f"Error when merging dataframes {error}")
                return

            # Continue with current dataframe
            df_current = df_merged

    logger.info("Completed Executor")


if __name__ == "__main__":
    executor()
