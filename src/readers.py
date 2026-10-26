import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def read_csv_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """Загружает финансовые операции из CSV-файла."""
    logger.info("Чтение CSV-файла: %s", file_path)

    try:
        data = pd.read_csv(file_path, sep=None, engine="python")
    except (FileNotFoundError, OSError, ValueError) as error:
        logger.error("Не удалось прочитать CSV-файл %s: %s", file_path, error)
        return []

    transactions = data.to_dict(orient="records")
    logger.info("Из CSV загружено операций: %s", len(transactions))
    return transactions  # type: ignore[return-value]


def read_excel_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """Загружает финансовые операции из Excel-файла."""
    logger.info("Чтение Excel-файла: %s", file_path)

    try:
        data = pd.read_excel(file_path)
    except (FileNotFoundError, OSError, ValueError, ImportError) as error:
        logger.error(
            "Не удалось прочитать Excel-файл %s: %s", file_path, error
        )
        return []

    transactions = data.to_dict(orient="records")
    logger.info("Из Excel загружено операций: %s", len(transactions))
    return transactions  # type: ignore[return-value]
