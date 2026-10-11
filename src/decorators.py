from collections.abc import Callable
from typing import Any, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def log(filename: str | None = None) -> Callable[[F], F]:
    """Логирует начало, результат и ошибки выполнения функции."""

    def decorator(func: F) -> F:
        """Добавляет логирование к функции."""

        def write_log(message: str) -> None:
            """Записывает сообщение в консоль или файл."""
            if filename is None:
                print(message)
            else:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(message + "\n")

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Выполняет функцию и записывает информацию о её работе."""
            write_log(f"{func.__name__} started")

            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = (
                    f"{func.__name__} error: "
                    f"{type(error).__name__}. Inputs: {args}, {kwargs}"
                )
                write_log(message)
                raise

            write_log(f"{func.__name__} ok. Result: {result}")
            return result

        return cast(F, wrapper)

    return decorator
