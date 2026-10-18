import json
from typing import Any


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Загружает список финансовых операций из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data

    return []
