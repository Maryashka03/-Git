from datetime import datetime

from .masks import get_mask_account, get_mask_card_number

def mask_account_card(account_card: str) -> str:
    """Маскирует номер карты или счета."""
    parts = account_card.split()
    number = "".join(parts[1:])

    if not number.isdigit():
        return "Некорректные данные"

    if parts[0].lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{parts[0]} {masked_number}"

def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ."""
    try:
        date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return date.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return "Некорректная дата"