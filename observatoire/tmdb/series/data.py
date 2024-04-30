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


def make_series_df(series_json: list[str]) -> pd.DataFrame:
    """
    Transforms the JSON data into a DataFrame
    """

    data = []
    unique_ids = set()

    for line in series_json:
        try:
            line_in_json = json.loads(line)

            safe_data = {}

            safe_data["adult"] = safe_bool(line_in_json, "adult")
            safe_data["backdrop_path"] = safe_str(line_in_json, "backdrop_path")
            safe_data["created_by"] = safe_list(line_in_json["created_by"], "name")
            safe_data["episode_run_time"] = safe_int(line_in_json, "episode_run_time")
            safe_data["first_air_date"] = safe_date(line_in_json, "first_air_date")
            safe_data["genres"] = safe_list(line_in_json["genres"], "name")
            safe_data["homepage"] = safe_str(line_in_json, "homepage")
            safe_data["id"] = safe_int(line_in_json, "id")
            safe_data["in_production"] = safe_bool(line_in_json, "in_production")
            safe_data["languages"] = safe_list(
                line_in_json["languages"],
                "english_name",
            )
            safe_data["last_air_date"] = safe_date(line_in_json, "last_air_date")
            safe_data["name"] = safe_str(line_in_json, "name")
            safe_data["networks"] = safe_list(
                line_in_json["networks"],
                "name",
            )
            safe_data["number_of_episodes"] = safe_int(line_in_json, "number_of_episodes")
            safe_data["number_of_seasons"] = safe_int(line_in_json, "number_of_seasons")
            safe_data["origin_country"] = safe_list(
                line_in_json["origin_country"],
                "name",
            )
            safe_data["original_language"] = safe_str(line_in_json, "original_language")
            safe_data["original_name"] = safe_str(line_in_json, "original_name")
            safe_data["overview"] = safe_str(line_in_json, "overview")
            safe_data["popularity"] = safe_float(line_in_json, "popularity")
            safe_data["poster_path"] = safe_str(line_in_json, "poster_path")
            safe_data["production_companies"] = safe_list(
                line_in_json["production_companies"],
                "name",
            )
            safe_data["production_countries"] = safe_list(
                line_in_json["production_countries"],
                "name",
            )
            safe_data["spoken_languages"] = safe_list(
                line_in_json["spoken_languages"],
                "english_name",
            )
            safe_data["status"] = safe_str(line_in_json, "status")
            safe_data["tagline"] = safe_str(line_in_json, "tagline")
            safe_data["type"] = safe_str(line_in_json, "type")
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
