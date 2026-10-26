from typing import Any

from src.processing import process_bank_search
from src.readers import read_csv_transactions, read_excel_transactions
from src.utils import load_transactions


def get_transactions(file_path: str, file_type: str) -> list[dict[str, Any]]:
    """Загружает операции из файла выбранного формата."""
    if file_type == "1":
        return load_transactions(file_path)
    if file_type == "2":
        return read_csv_transactions(file_path)
    if file_type == "3":
        return read_excel_transactions(file_path)
    return []


def filter_by_status(
    transactions: list[dict[str, Any]], status: str
) -> list[dict[str, Any]]:
    """Оставляет операции с выбранным статусом."""
    if not status:
        return transactions

    return [
        transaction
        for transaction in transactions
        if str(transaction.get("state", "")).upper() == status.upper()
    ]


def filter_by_currency(
    transactions: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Оставляет операции в рублях."""
    result = []

    for transaction in transactions:
        amount = transaction.get("operationAmount", {})
        currency = amount.get("currency", {}) if isinstance(amount, dict) else {}
        code = currency.get("code", "") if isinstance(currency, dict) else ""

        if code == "RUB" or transaction.get("currency_code") == "RUB":
            result.append(transaction)

    return result


def sort_by_date(
    transactions: list[dict[str, Any]], ascending: bool = True
) -> list[dict[str, Any]]:
    """Сортирует операции по дате."""
    return sorted(
        transactions,
        key=lambda transaction: str(transaction.get("date", "")),
        reverse=not ascending,
    )


def main() -> None:
    """Запускает пользовательское меню обработки операций."""
    print("Выберите формат файла:")
    print("1 — JSON")
    print("2 — CSV")
    print("3 — Excel")

    file_type = input("Ваш выбор: ").strip()
    if file_type not in {"1", "2", "3"}:
        print("Неизвестный формат файла.")
        return

    file_path = input("Введите путь к файлу: ").strip().strip('"')
    transactions = get_transactions(file_path, file_type)

    if not transactions:
        print("Операции не найдены или файл не удалось прочитать.")
        return

    print("Выберите статус: EXECUTED, CANCELED, PENDING")
    print("Или нажмите Enter, чтобы пропустить фильтр.")
    status = input("Статус: ").strip().upper()

    if status and status not in {"EXECUTED", "CANCELED", "PENDING"}:
        print("Неизвестный статус.")
        return

    transactions = filter_by_status(transactions, status)

    sort_choice = input("Сортировать по дате? (да/нет): ").strip().lower()
    if sort_choice in {"да", "д", "yes", "y"}:
        direction = input("По возрастанию? (да/нет): ").strip().lower()
        ascending = direction in {"да", "д", "yes", "y"}
        transactions = sort_by_date(transactions, ascending)

    rubles_only = input("Показывать только рублёвые операции? (да/нет): ")
    if rubles_only.strip().lower() in {"да", "д", "yes", "y"}:
        transactions = filter_by_currency(transactions)

    search = input("Поиск по описанию (Enter — пропустить): ").strip()
    if search:
        transactions = process_bank_search(transactions, search)

    if not transactions:
        print("По заданным условиям операции не найдены.")
        return

    print(f"Найдено операций: {len(transactions)}")
    for transaction in transactions:
        print(transaction)


if __name__ == "__main__":
    main()
