from datetime import UTC, datetime
from pathlib import Path

# Get current working directory
cwd = Path.cwd()

# Define folder paths
DATA_FOLDER = Path(cwd) / ".tmdb_cache"
DATA_FILE = Path(DATA_FOLDER) / "tmdb_data.parquet"
ARCHIVE_FOLDER = Path(DATA_FOLDER) / "archive"
OUTPUT_FOLDER = Path(DATA_FOLDER) / "output"
LOG_FILE_PATH = Path(DATA_FOLDER) / "logs"
SAVED_MOVIE_TRACKER_PATH = Path(ARCHIVE_FOLDER) / "completed_movie_ids.txt"

# Create necessary folders if they don't exist
Path.mkdir(DATA_FOLDER, exist_ok=True, parents=True)
Path.mkdir(OUTPUT_FOLDER, exist_ok=True, parents=True)
Path.mkdir(LOG_FILE_PATH, exist_ok=True, parents=True)
Path.mkdir(ARCHIVE_FOLDER, exist_ok=True, parents=True)

# Get current date
now = datetime.now(UTC).date()

# Create file path for saving json file
JSON_SAVE_FILE_PATH = Path(ARCHIVE_FOLDER) / f"{now}_TMDB_movies.ndjson"
