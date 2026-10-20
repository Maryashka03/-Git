import json
import logging
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    "logs/utils.log", mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Загружает список финансовых операций из JSON-файла."""
    logger.debug("Начало загрузки файла %s", file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        return []
    except json.JSONDecodeError:
        logger.error("Ошибка чтения JSON-файла: %s", file_path)
        return []

    if isinstance(data, list) and all(
        isinstance(item, dict) for item in data
    ):
        logger.info("Файл успешно загружен: %s", file_path)
        return data

    logger.error("Некорректный формат данных в файле: %s", file_path)
    return []
