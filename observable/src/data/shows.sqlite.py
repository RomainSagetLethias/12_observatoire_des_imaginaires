import os
import sqlite3
import tempfile
from datetime import datetime

import pandas as pd

with tempfile.TemporaryDirectory() as temp_dir:
    os.chdir(temp_dir)

    os.system(
        "kaggle datasets download -d asaniczka/full-tmdb-tv-shows-dataset-2023-150k-shows >&2",
    )
    os.system("unzip full-tmdb-tv-shows-dataset-2023-150k-shows.zip >&2")

    df = pd.read_csv("TMDB_tv_dataset_v3.csv", parse_dates=["first_air_date"])

    # Remove adult movies
    df = df[df["adult"] == False]  # noqa: E712

    # Remove documentaries
    df = df[df["genres"].str.contains("Documentary") == False]  # noqa: E712

    # Remove shows with a future first air date or no first air date
    now = datetime.now()
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
            df.to_sql("shows", conn, index=False)

    # Print db file to stdout
    os.system(f"cat {temp_filename}")
