import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_MAX_RETRIES = int(os.getenv("TMDB_MAX_RETRIES", "500"))