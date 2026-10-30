import json

import pandas as pd


def simple_search(
    transactions: pd.DataFrame,
    search_query: str,
) -> str:
    """Ищет операции по описанию или категории."""
    if not search_query.strip():
        return json.dumps([], ensure_ascii=False)

    query = search_query.strip().casefold()

    descriptions = transactions["Описание"].fillna("").astype(str)
    categories = transactions["Категория"].fillna("").astype(str)

    mask = (
        descriptions.str.casefold().str.contains(query, regex=False)
        | categories.str.casefold().str.contains(query, regex=False)
    )

    result = transactions.loc[mask].copy()

    result = result.where(pd.notna(result), None)

    return result.to_json(
        orient="records",
        force_ascii=False,
        date_format="iso",
    )
