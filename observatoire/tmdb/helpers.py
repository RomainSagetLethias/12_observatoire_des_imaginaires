import json


def parse_keywords(keywords: str) -> str:
    """
    Parses the keywords into a list
    """

    keywords_dict = json.loads(keywords)

    keywords_list = []

    for item in keywords_dict["keywords"]:
        keywords_list.append(item["name"])

    return ", ".join(keywords_list)
