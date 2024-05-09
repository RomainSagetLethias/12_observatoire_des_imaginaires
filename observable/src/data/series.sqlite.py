import os
import sqlite3
import tempfile
from datetime import datetime

from observatoire.tmdb.series.hf import load_series_dataset

# Load the dataset
df = load_series_dataset()

# Remove adult movies
df = df[df["adult"] == False]  # noqa: E712

# Remove documentaries
df = df[df["genres"].str.contains("Documentary") == False]  # noqa: E712

# Remove shows with a future first air date or no first air date
now = datetime.now().strftime("%Y-%m-%d")
df = df[df["first_air_date"] < now]

# Select the columns we want
df = df[["id", "name", "original_name", "poster_path"]]

# Set original name to blank string if same as name
df["original_name"] = df["original_name"].where(
    df["name"] != df["original_name"],
    "",
)

# Save the dataframe to a SQLite database
with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as temp_file:
    temp_filename = temp_file.name
    with sqlite3.connect(temp_filename) as conn:
        df.to_sql("series", conn, index=False)

# Print db file to stdout
os.system(f"cat {temp_filename}")
