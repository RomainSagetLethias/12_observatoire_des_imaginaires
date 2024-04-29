import json

import pandas as pd

from observatoire.tmdb.data import (
    safe_bool,
    safe_date,
    safe_float,
    safe_int,
    safe_list,
    safe_str,
)


def transform_movie_json(movie_json: list[str]) -> pd.DataFrame:
    """
    Transforms the JSON data into a DataFrame
    """

    data = []
    unique_ids = set()

    for line in movie_json:
        try:
            line_in_json = json.loads(line)

            formatted_data = {}

            formatted_data["genres"] = safe_list(line_in_json, "genres")
            formatted_data["spoken_languages"] = safe_list(line_in_json, "spoken_languages")
            formatted_data["adult"] = safe_bool(line_in_json, "adult")
            formatted_data["backdrop_path"] = safe_str(line_in_json, "backdrop_path")
            formatted_data["budget"] = safe_int(line_in_json, "budget")
            formatted_data["homepage"] = safe_str(line_in_json, "homepage")
            formatted_data["id"] = (
                int(line_in_json["id"]) if line_in_json["id"] is not None else 0
            )
            formatted_data["imdb_id"] = safe_str(line_in_json, "imdb_id")
            formatted_data["keywords"] = safe_str(line_in_json, "keywords")
            formatted_data["original_language"] = safe_str(line_in_json, "original_language")
            formatted_data["original_title"] = safe_str(line_in_json, "original_title")
            formatted_data["overview"] = safe_str(line_in_json, "overview")
            formatted_data["popularity"] = safe_float(line_in_json, "popularity")
            formatted_data["poster_path"] = safe_str(line_in_json, "poster_path")
            formatted_data["production_companies"] = safe_list(
                line_in_json,
                "production_companies",
            )
            formatted_data["production_countries"] = safe_list(
                line_in_json,
                "production_countries",
            )
            formatted_data["release_date"] = safe_date(line_in_json, "release_date")
            formatted_data["revenue"] = safe_int(line_in_json, "revenue")
            formatted_data["runtime"] = safe_int(line_in_json, "runtime")
            formatted_data["status"] = safe_str(line_in_json, "status")
            formatted_data["tagline"] = safe_str(line_in_json, "tagline")
            formatted_data["title"] = safe_str(line_in_json, "title")
            formatted_data["vote_average"] = safe_float(line_in_json, "vote_average")
            formatted_data["vote_count"] = safe_int(line_in_json, "vote_count")
        except Exception:
            continue

        # remove and newline chracters
        updated_data = {}
        for key, value in formatted_data.items():
            if isinstance(value, str):  # Check if the value is a string
                updated_value = value.replace("\n", " ").replace("\r", " ")
                updated_data[key] = updated_value
            else:
                updated_data[key] = value

        # add the data to our local list
        if updated_data["id"] not in unique_ids:
            unique_ids.add(updated_data["id"])
            data.append(updated_data)

    return pd.DataFrame(data)
