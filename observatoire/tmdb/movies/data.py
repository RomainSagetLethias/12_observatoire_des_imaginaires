import json

import pandas as pd


def transform_movie_json(movie_json: list[str]) -> pd.DataFrame:  # noqa: C901, PLR0915
    """
    Transforms the JSON data into a DataFrame
    """

    data = []
    unique_ids = set()

    # load the data
    variations_to_ignore = [
        None,
        "",
        "NA",
        "N/A",
        "None",
        "na",
        "n/a",
        "NULL",
        "Not Available",
    ]

    for line in movie_json:
        line_in_json = json.loads(line)

        # TODO: format_list_to_str is too complex and should be refactored
        def format_list_to_str(line_in_json: dict, formatted_data: dict) -> dict:  # noqa: C901, PLR0912
            # convert genres list to str

            genres_str = None
            genres_list = []
            try:
                for genre in line_in_json["genres"]:
                    if genre["name"] is not any(variations_to_ignore):
                        genres_list.append(genre["name"])
                if len(genres_list) > 0:
                    genres_str = ", ".join(genres_list)
            except Exception:
                pass

            formatted_data["genres"] = genres_str

            # convert production_companies list to str
            production_companies_str = None
            production_companies_list = []
            try:
                for company in line_in_json["production_companies"]:
                    if company["name"] is not any(variations_to_ignore):
                        production_companies_list.append(company["name"])
                if len(production_companies_list) > 0:
                    production_companies_str = ", ".join(production_companies_list)
            except Exception:
                pass

            formatted_data["production_companies"] = production_companies_str

            # convert production_countries list to str
            production_countries_str = None
            production_countries_list = []
            try:
                for country in line_in_json["production_countries"]:
                    if country["name"] is not any(variations_to_ignore):
                        production_countries_list.append(country["name"])
                if len(production_countries_list) > 0:
                    production_countries_str = ", ".join(production_countries_list)
            except Exception:
                pass

            formatted_data["production_countries"] = production_countries_str

            # convert spoken_languages list to str
            spoken_languages_str = None
            spoken_languages_list = []
            try:
                for language in line_in_json["spoken_languages"]:
                    if language["english_name"] is not any(variations_to_ignore):
                        spoken_languages_list.append(language["english_name"])
                if len(spoken_languages_list) > 0:
                    spoken_languages_str = ", ".join(spoken_languages_list)
            except Exception:
                pass

            formatted_data["spoken_languages"] = spoken_languages_str

            return formatted_data

        # format the data

        formatted_data = {}

        formatted_data["id"] = int(line_in_json["id"]) if line_in_json["id"] is not None else 0

        formatted_data["title"] = (
            str(line_in_json["title"])
            if line_in_json["title"] is not any(variations_to_ignore)
            else None
        )
        formatted_data["vote_average"] = (
            float(line_in_json["vote_average"])
            if line_in_json["vote_average"] is not None
            else 0.0
        )

        formatted_data["vote_count"] = (
            int(line_in_json["vote_count"]) if line_in_json["vote_count"] is not None else 0
        )

        formatted_data["status"] = (
            str(line_in_json["status"])
            if line_in_json["status"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["release_date"] = (
            str(line_in_json["release_date"])
            if line_in_json["release_date"] is not None and line_in_json["release_date"] != ""
            else "1500-01-01"
        )

        formatted_data["revenue"] = (
            int(line_in_json["revenue"]) if line_in_json["revenue"] is not None else 0
        )

        formatted_data["runtime"] = (
            int(line_in_json["runtime"]) if line_in_json["runtime"] is not None else 0
        )

        formatted_data["adult"] = (
            bool(line_in_json["adult"]) if line_in_json["adult"] is not None else False
        )

        formatted_data["backdrop_path"] = (
            str(line_in_json["backdrop_path"])
            if line_in_json["backdrop_path"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["budget"] = (
            int(line_in_json["budget"]) if line_in_json["budget"] is not None else 0
        )

        formatted_data["homepage"] = (
            str(line_in_json["homepage"])
            if line_in_json["homepage"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["imdb_id"] = (
            str(line_in_json["imdb_id"])
            if line_in_json["imdb_id"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["original_language"] = (
            str(line_in_json["original_language"])
            if line_in_json["original_language"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["original_title"] = (
            str(line_in_json["original_title"])
            if line_in_json["original_title"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["overview"] = (
            str(line_in_json["overview"])
            if line_in_json["overview"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["popularity"] = (
            float(line_in_json["popularity"]) if line_in_json["popularity"] is not None else 0.0
        )

        formatted_data["poster_path"] = (
            str(line_in_json["poster_path"])
            if line_in_json["poster_path"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["tagline"] = (
            str(line_in_json["tagline"])
            if line_in_json["tagline"] is not any(variations_to_ignore)
            else None
        )

        formatted_data["keywords"] = str(line_in_json["keywords"])
        try:
            final_formatted_data = format_list_to_str(line_in_json, formatted_data)
        except Exception:
            continue

        # remove and newline chracters
        updated_data = {}
        for key, value in final_formatted_data.items():
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
