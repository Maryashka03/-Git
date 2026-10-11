import pytest

from src.decorators import log


def test_log_success_to_console(capsys):
    """Проверяет логирование начала и результата в консоль."""

    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert "add started" in captured.out
    assert "add ok. Result: 3" in captured.out


def test_log_success_to_file(tmp_path):
    """Проверяет запись начала и результата в файл."""
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(x, y):
        return x + y

    assert add(1, 2) == 3
    content = log_file.read_text(encoding="utf-8")

    assert "add started" in content
    assert "add ok. Result: 3" in content


def test_log_error_to_console(capsys):
    """Проверяет логирование ошибки и входных аргументов."""

    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()

    assert "divide started" in captured.out
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


def test_log_error_to_file(tmp_path):
    """Проверяет запись ошибки в файл."""
    log_file = tmp_path / "errors.txt"

    @log(filename=str(log_file))
    def fail(value):
        raise ValueError("bad value")

    with pytest.raises(ValueError):
        fail(10)

    content = log_file.read_text(encoding="utf-8")

    assert "fail started" in content
    assert "fail error: ValueError" in content
    assert "Inputs: (10,), {}" in content


def test_log_keyword_arguments(capsys):
    """Проверяет запись именованных аргументов при ошибке."""

    @log()
    def fail(value, *, mode):
        raise ValueError("bad value")

    with pytest.raises(ValueError):
        fail(10, mode="test")

    captured = capsys.readouterr()

    assert "Inputs: (10,), {'mode': 'test'}" in captured.out
