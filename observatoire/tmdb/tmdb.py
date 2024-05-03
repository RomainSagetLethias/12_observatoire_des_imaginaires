def parse_keywords(keywords: dict) -> str:
    """
    Parses the keywords into a list
    """

    keywords_list = [item["name"] for item in keywords]

    return ", ".join(keywords_list)
