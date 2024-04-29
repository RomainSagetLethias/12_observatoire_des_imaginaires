import os
import sqlite3
import tempfile
from datetime import datetime

from observatoire.tmdb.movies.hf import load_movies_dataset

# Load the dataset
df = load_movies_dataset()

# Remove adult movies
df = df[df["adult"] == False]  # noqa: E712

# Remove documentaries
df = df[df["genres"].str.contains("Documentary") == False]  # noqa: E712

# Remove movies with a future release date
now = datetime.now().strftime("%Y-%m-%d")
df = df[df["release_date"] < now]

# Remove movies with no known revenue
# and original_language other than EU languages
df = df[
    (df["revenue"] == 0)
    & (
        df["original_language"].isin(
            [
                "cs",
                "da",
                "de",
                "en",
                "es",
                "et",
                "fi",
                "fr",
                "hr",
                "hu",
                "is",
                "it",
                "lt",
                "lv",
                "nl",
                "no",
                "pl",
                "pt",
                "ro",
                "sl",
                "sv",
            ],
        )
    )
    | (df["revenue"] > 0)
]

# Add a column with the production_year based on the release_date
df["production_year"] = df["release_date"].str[:4]

# Select the columns we want
df = df[
    [
        "id",
        "title",
        "original_title",
        "production_year",
        "poster_path",
    ]
]

# Set original title to blank string if same as title
df["original_title"] = df["original_title"].where(df["title"] != df["original_title"], "")

# Save the dataframe to a SQLite database
with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as temp_file:
    temp_filename = temp_file.name
    with sqlite3.connect(temp_filename) as conn:
        df.to_sql("films", conn, index=False)

# Print db file to stdout
os.system(f"cat {temp_filename}")
