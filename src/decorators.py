from collections.abc import Callable
from typing import Any, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def log(filename: str | None = None) -> Callable[[F], F]:
    """Логирует успешное выполнение функции или возникшую ошибку."""

    def decorator(func: F) -> F:
        """Добавляет логирование к функции."""

        func

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Выполняет функцию и записывает результат или ошибку."""
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = (
                    f"{func.__name__} error: "
                    f"{type(error).__name__}. Inputs: {args}, {kwargs}"
                )
                if filename is None:
                    print(message)
                else:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                raise

            message = f"{func.__name__} ok"
            if filename is None:
                print(message)
            else:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(message + "\n")

            return result

        return cast(F, wrapper)

    return decorator
