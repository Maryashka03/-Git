import re
from collections import Counter
from typing import Any


def process_bank_search(
    data: list[dict[str, Any]], search: str
) -> list[dict[str, Any]]:
    """Ищет операции по тексту в описании."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        transaction
        for transaction in data
        if pattern.search(str(transaction.get("description", "")))
    ]


def process_bank_operations(
    data: list[dict[str, Any]], categories: list[str]
) -> dict[str, int]:
    """Считает операции, содержащие указанные категории в описании."""
    counts = Counter()
    for category in categories:
        counts[category] = sum(
            1
            for transaction in data
            if category.casefold()
            in str(transaction.get("description", "")).casefold()
        )
    return dict(counts)
