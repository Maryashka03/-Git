from src.processing import process_bank_operations, process_bank_search

TRANSACTIONS = [
    {
        "description": "Перевод клиенту",
        "amount": 1000,
    },
    {
        "description": "Оплата супермаркета",
        "amount": 500,
    },
    {
        "description": "Перевод между счетами",
        "amount": 2000,
    },
]


def test_process_bank_search_finds_matching_transactions():
    result = process_bank_search(TRANSACTIONS, "перевод")

    assert len(result) == 2
    assert all("перевод" in item["description"].casefold() for item in result)


def test_process_bank_search_is_case_insensitive():
    result = process_bank_search(TRANSACTIONS, "СУПЕРМАРКЕТ")

    assert len(result) == 1
    assert result[0]["amount"] == 500


def test_process_bank_search_returns_empty_list_when_not_found():
    result = process_bank_search(TRANSACTIONS, "авиабилеты")

    assert result == []


def test_process_bank_operations_counts_categories():
    result = process_bank_operations(
        TRANSACTIONS,
        ["перевод", "супермаркет", "авиабилеты"],
    )

    assert result == {
        "перевод": 2,
        "супермаркет": 1,
        "авиабилеты": 0,
    }


def test_process_bank_operations_is_case_insensitive():
    result = process_bank_operations(
        TRANSACTIONS,
        ["ПЕРЕВОД"],
    )

    assert result == {"ПЕРЕВОД": 2}


def test_process_bank_operations_with_empty_data():
    result = process_bank_operations([], ["перевод"])

    assert result == {"перевод": 0}
