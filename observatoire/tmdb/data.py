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


def safe_list(values: dict, field_name: str, key: str) -> str:
    # convert spoken_languages list to str
    result_list = []
    try:
        for val in values[field_name]:
            if isinstance(val, dict) and val[key] is not any(VARIATIONS_TO_IGNORE):
                result_list.append(val[key])
            elif val is not any(VARIATIONS_TO_IGNORE):
                result_list.append(val)
    except Exception:
        pass

    return ", ".join(result_list) if len(result_list) > 0 else ""


def safe_int(values: dict, field_name: str) -> int:
    # use first value if values[field_name] is a list
    val = (
        values[field_name][0]
        if isinstance(values[field_name], list) and len(values[field_name]) > 0
        else values[field_name]
    )
    return int(val) if val is not None else 0


def safe_float(values: dict, field_name: str) -> float:
    return float(values[field_name]) if values[field_name] is not None else 0.0


def safe_str(values: dict, field_name: str) -> str:
    val = values[field_name] if values[field_name] is not None else ""
    return str(val) if val is not any(VARIATIONS_TO_IGNORE) else ""


def safe_bool(values: dict, field_name: str) -> bool:
    return bool(values[field_name]) if values[field_name] is not None else False


def safe_date(values: dict, field_name: str) -> str:
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
