import json

from src.utils import load_transactions


def test_load_transactions_returns_list_of_dicts(tmp_path):
    file_path = tmp_path / "operations.json"
    transactions = [{"id": 1}, {"id": 2}]
    file_path.write_text(json.dumps(transactions), encoding="utf-8")
    assert load_transactions(str(file_path)) == transactions


def test_load_transactions_returns_empty_list_for_empty_file(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text("", encoding="utf-8")
    assert load_transactions(str(file_path)) == []


def test_load_transactions_returns_empty_list_for_missing_file(tmp_path):
    file_path = tmp_path / "missing.json"
    assert load_transactions(str(file_path)) == []


def test_load_transactions_returns_empty_list_for_non_list_json(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    assert load_transactions(str(file_path)) == []


def test_load_transactions_returns_empty_list_for_invalid_json(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text("{invalid json", encoding="utf-8")
    assert load_transactions(str(file_path)) == []
