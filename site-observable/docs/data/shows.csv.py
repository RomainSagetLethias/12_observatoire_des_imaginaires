import os
import tempfile

import pandas as pd

with tempfile.TemporaryDirectory() as temp_dir:
    os.chdir(temp_dir)

    os.system(
        "kaggle datasets download -d asaniczka/full-tmdb-tv-shows-dataset-2023-150k-shows >&2",
    )
    os.system("unzip full-tmdb-tv-shows-dataset-2023-150k-shows.zip >&2")

    df = pd.read_csv("TMDB_tv_dataset_v3.csv")

    # Remove adult movies
    df = df[df["adult"] == False]  # noqa: E712

    # Add a column with the tally URL
    df["tally_url"] = df.apply(
        lambda row: f"""https://tally.so/r/wQ5Og8?original_title={row["original_name"]}&production_countries={row["production_countries"]}""",
        axis=1,
    )

    # Select the columns we want
    df = df[["id", "name", "tally_url"]]

    print(df.to_csv(index=False))
