import json

import pandas as pd

from observatoire.tmdb.data import (
    remove_newline_characters,
    safe_bool,
    safe_date,
    safe_float,
    safe_int,
    safe_list,
    safe_str,
)


def make_movie_df(movie_json: list[str]) -> pd.DataFrame:
    """
    Transforms the JSON data into a DataFrame
    """

    data = []
    unique_ids = set()

    for line in movie_json:
        try:
            line_in_json = json.loads(line)

            safe_data = {}

            safe_data["adult"] = safe_bool(line_in_json, "adult")
            safe_data["backdrop_path"] = safe_str(line_in_json, "backdrop_path")
            safe_data["budget"] = safe_int(line_in_json, "budget")
            safe_data["genres"] = safe_list(line_in_json, "genres", "name")
            safe_data["homepage"] = safe_str(line_in_json, "homepage")
            safe_data["id"] = safe_int(line_in_json, "id")
            safe_data["imdb_id"] = safe_str(line_in_json, "imdb_id")
            safe_data["keywords"] = safe_str(line_in_json, "keywords")
            safe_data["original_language"] = safe_str(line_in_json, "original_language")
            safe_data["original_title"] = safe_str(line_in_json, "original_title")
            safe_data["overview"] = safe_str(line_in_json, "overview")
            safe_data["popularity"] = safe_float(line_in_json, "popularity")
            safe_data["poster_path"] = safe_str(line_in_json, "poster_path")
            safe_data["production_companies"] = safe_list(
                line_in_json,
                "production_companies",
                "name",
            )
            safe_data["production_countries"] = safe_list(
                line_in_json,
                "production_countries",
                "name",
            )
            safe_data["release_date"] = safe_date(line_in_json, "release_date")
            safe_data["revenue"] = safe_int(line_in_json, "revenue")
            safe_data["runtime"] = safe_int(line_in_json, "runtime")
            safe_data["spoken_languages"] = safe_list(
                line_in_json,
                "spoken_languages",
                "english_name",
            )
            safe_data["status"] = safe_str(line_in_json, "status")
            safe_data["tagline"] = safe_str(line_in_json, "tagline")
            safe_data["title"] = safe_str(line_in_json, "title")
            safe_data["vote_average"] = safe_float(line_in_json, "vote_average")
            safe_data["vote_count"] = safe_int(line_in_json, "vote_count")
        except Exception:
            continue

        # remove and newline chracters
        safe_data = remove_newline_characters(safe_data)

        # add the data to our local list
        if safe_data["id"] not in unique_ids:
            unique_ids.add(safe_data["id"])
            data.append(safe_data)

    return pd.DataFrame(data)
