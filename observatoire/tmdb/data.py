VARIATIONS_TO_IGNORE = [
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


def safe_list(values: dict, field_name: str) -> str | None:
    # convert spoken_languages list to str
    result = None
    result_list = []
    try:
        for val in values:
            if val[field_name] is not any(VARIATIONS_TO_IGNORE):
                result_list.append(val[field_name])
        if len(result_list) > 0:
            result = ", ".join(result_list)
    except Exception:
        pass

    return result


def safe_int(values: dict, field_name: str) -> int | None:
    return int(values[field_name]) if values[field_name] is not None else 0


def safe_float(values: dict, field_name: str) -> float | None:
    return float(values[field_name]) if values[field_name] is not None else 0.0


def safe_str(values: dict, field_name: str) -> str | None:
    return (
        str(values[field_name]) if values[field_name] is not any(VARIATIONS_TO_IGNORE) else None
    )


def safe_bool(values: dict, field_name: str) -> bool | None:
    return bool(values[field_name]) if values[field_name] is not None else False


def safe_date(values: dict, field_name: str) -> str | None:
    return (
        str(values[field_name])
        if values[field_name] is not None and values[field_name] != ""
        else "1500-01-01"
    )


def remove_newline_characters(formatted_data: dict) -> dict:
    updated_data = {}
    for key, value in formatted_data.items():
        if isinstance(value, str):  # Check if the value is a string
            updated_value = value.replace("\n", " ").replace("\r", " ")
            updated_data[key] = updated_value
        else:
            updated_data[key] = value
    return updated_data
