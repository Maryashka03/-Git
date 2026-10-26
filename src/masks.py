import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    "logs/masks.log", mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер карты."""
    logger.debug("Начало маскирования номера карты")
    digits = "".join(char for char in card_number if char.isdigit())

    if len(digits) < 16:
        logger.error("Некорректный номер карты")
        return "Некорректный номер карты"

    result = f"{digits[:4]} {digits[4:6]}** **** {digits[12:16]}"
    logger.info("Номер карты успешно замаскирован")
    return result


def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный номер счёта."""
    logger.debug("Начало маскирования номера счёта")
    digits = "".join(char for char in account_number if char.isdigit())

    if len(digits) < 4:
        logger.error("Некорректный номер счета")
        return "Некорректный номер счета"

    result = f"**{digits[-4:]}"
    logger.info("Номер счёта успешно замаскирован")
    return result
