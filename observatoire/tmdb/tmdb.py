import json
import logging
import threading
import time
from http import HTTPStatus

import requests
from tqdm import tqdm

from observatoire.tmdb.config import TMDB_API_KEY, TMDB_MAX_RETRIES
from observatoire.tmdb.helpers import parse_keywords

lock = threading.Lock()
FULL_LOG = False  # Mark True to log everything


def get_latest_movie_id() -> int:
    """
    Get the ID of the latest movie added to the TMDB database.
    """
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


def handler_get_keywords(movie_id: int) -> list[int, str]:
    """
    handles getting keywords
    """

    data = get_keywords(movie_id)

    if not data:
        return None

    keywords_str = parse_keywords(data)

    return keywords_str


def get_movie_data(
    movie_json: list[str],
    movie_id: int,
    logger: logging,
    pbar: tqdm,
) -> None:
    if FULL_LOG:
        logger.info(f"Processing {movie_id}")

    with lock:
        pbar.update(1)

    try:
        time.sleep(0.2)
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=fr-FR&region=FR"
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
            movie_json.append(json.dumps(rqst_json))

            if FULL_LOG:
                logger.info(f"movies collected: {len(movie_json)}")

    except Exception:
        logger.exception(f"Expection for {movie_id} in process_movie_ids")

    if FULL_LOG:
        logger.info(f"Completed movie {movie_id}")
