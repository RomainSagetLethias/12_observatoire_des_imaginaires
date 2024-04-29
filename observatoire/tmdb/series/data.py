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


def transform_series_json(series_json: list[str]) -> pd.DataFrame:
    """
    Transforms the JSON data into a DataFrame
    """

    data = []
    unique_ids = set()

    for line in series_json:
        try:
            line_in_json = json.loads(line)

            # format the data

            formatted_data = {}

            formatted_data["adult"] = safe_bool(line_in_json, "adult")
            formatted_data["backdrop_path"] = safe_str(line_in_json, "backdrop_path")
            formatted_data["created_by"] = safe_list(line_in_json["created_by"], "name")
            formatted_data["episode_run_time"] = safe_int(line_in_json, "episode_run_time")
            formatted_data["first_air_date"] = safe_date(line_in_json, "first_air_date")
            formatted_data["genres"] = safe_list(line_in_json["genres"], "name")
            formatted_data["homepage"] = safe_str(line_in_json, "homepage")
            formatted_data["id"] = safe_int(line_in_json, "id")
            formatted_data["in_production"] = safe_bool(line_in_json, "in_production")
            formatted_data["languages"] = safe_list(
                line_in_json["languages"],
                "english_name",
            )
            formatted_data["last_air_date"] = safe_date(line_in_json, "last_air_date")
            formatted_data["name"] = safe_str(line_in_json, "name")
            formatted_data["networks"] = safe_list(
                line_in_json["networks"],
                "name",
            )
            formatted_data["number_of_episodes"] = safe_int(line_in_json, "number_of_episodes")
            formatted_data["number_of_seasons"] = safe_int(line_in_json, "number_of_seasons")
            formatted_data["origin_country"] = safe_list(
                line_in_json["origin_country"],
                "name",
            )
            formatted_data["original_language"] = safe_str(line_in_json, "original_language")
            formatted_data["original_name"] = safe_str(line_in_json, "original_name")
            formatted_data["overview"] = safe_str(line_in_json, "overview")
            formatted_data["popularity"] = safe_float(line_in_json, "popularity")
            formatted_data["poster_path"] = safe_str(line_in_json, "poster_path")
            formatted_data["production_companies"] = safe_list(
                line_in_json["production_companies"],
                "name",
            )
            formatted_data["production_countries"] = safe_list(
                line_in_json["production_countries"],
                "name",
            )
            formatted_data["spoken_languages"] = safe_list(
                line_in_json["spoken_languages"],
                "english_name",
            )
            formatted_data["status"] = safe_str(line_in_json, "status")
            formatted_data["tagline"] = safe_str(line_in_json, "tagline")
            formatted_data["type"] = safe_str(line_in_json, "type")
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
