import pandas as pd

def prepare_technology_data(data, colname_id):
    """
    Extracts and prepares technology-related data for analysis from multiple characters.

    Parameters:
        data (DataFrame): The original dataset containing technology tools and demographic 
        information for characters.
        colname_id (String): Part of the column name for which we want to do the analysis, 
        e.g. 'gender'.

    Returns:
        DataFrame: A long-format DataFrame ready for analysis and visualization.
    """
    # Technology tools as described in the dataset
    tech_tools_suffix = [
        "Smartphone",
        "Ordinateur",
        "TV",
        "Tablette",
        "Console de jeux",
        "Objets connectés",
        "Robotique",
        "Autre",
    ]

    # Prepare and concatenate data for all characters with accurate column names
    all_characters_data = pd.DataFrame()

    # Loop through each character number
    for i in range(1, 5):
        # Prepare the mapping for each character's technology columns using the correct format
        colnames = {
            f"character{i}_technology_tools [{tool}]": tool
            for tool in tech_tools_suffix
        }
        colnames[f"character{i}_" + colname_id] = colname_id

        # Select and rename the relevant columns for each character
        temp_data = data[list(colnames.keys())].rename(columns=colnames)

        # Append to the overall DataFrame
        all_characters_data = pd.concat(
            [all_characters_data, temp_data], ignore_index=True
        )

    # Melt the DataFrame to long format for easier plotting
    melted_data_all = all_characters_data.melt(
        id_vars=[colname_id],
        value_vars=tech_tools_suffix,
        var_name="Technology",
        value_name="Frequency",
    )

    # Remove NaN entries for plotting
    melted_data_all.dropna(inplace=True)

    return melted_data_all


# Example usage:
# df = pd.read_csv('your_dataset.csv')
# prepared_data = prepare_technology_data(df)
# print(prepared_data.head())


def prepare_character_data(data, colname_suffixes):
    """
    Extracts and prepares data for analysis from multiple characters.

    Parameters:
        data (DataFrame): The original dataset containing technology tools and demographic 
        information for characters.
        colname_id (String): Part of the column name for which we want to do the analysis, 
        e.g. 'gender'.

    Returns:
        DataFrame: A long-format DataFrame ready for analysis and visualization.
    """

    # Prepare and concatenate data for all characters with accurate column names
    all_characters_data = pd.DataFrame()

    # Loop through each character number
    for i in range(1, 5):
        # Prepare the mapping for each character's technology columns using the correct format
        colnames = {f"character{i}_{suffix}": suffix for suffix in colname_suffixes}

        # Select and rename the relevant columns for each character
        temp_data = data[list(colnames.keys())].rename(columns=colnames)

        # Append to the overall DataFrame
        all_characters_data = pd.concat(
            [all_characters_data, temp_data], ignore_index=True
        )

    return all_characters_data


import re


def extract_text_between_brackets(string):
    # Regular expression pattern to find text between [ and (
    # This is useful for extracting short labels for the environmental issues

    # \[  -> match the character '[' literally
    # (   -> start capturing group
    # [^\[\(]+ -> match any character except '[' or '(' one or more times
    # )   -> end capturing group
    # \)  -> match the character '(' literally
    match = re.search(r"\[([^\[\(]+)\(", string)

    if match:
        return match.group(
            1
        ).strip()  # Return the matched group and strip any extra whitespace
    return None  # Return None if no match is found

