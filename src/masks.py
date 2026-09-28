def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер карты."""
    digits = "".join(char for char in card_number if char.isdigit())

    if len(digits) < 16:
        return "Некорректный номер карты"

    return f"{digits[:4]} {digits[4:6]}** **** {digits[12:16]}"

def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный номер счета."""
    digits = "".join(char for char in account_number if char.isdigit())

    if len(digits) < 4:
        return "Некорректный номер счета"

    return f"**{digits[-4:]}"
