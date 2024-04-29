import os

HF_MOVIES_DATASET = "DataForGood/observatoire_des_imaginaires_movies"
HF_SERIES_DATASET = "DataForGood/observatoire_des_imaginaires_series"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_MAX_RETRIES = int(os.getenv("TMDB_MAX_RETRIES", "500"))
TMDB_BATCH_SIZE = int(os.getenv("TMDB_BATCH_SIZE", "10000"))
