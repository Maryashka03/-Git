Bank Widget

Учебный проект для загрузки, обработки и поиска банковских операций.

Возможности

- Загрузка банковских операций из файлов JSON, CSV и Excel.
- Фильтрация операций по статусу.
- Сортировка операций по дате.
- Фильтрация операций в российских рублях.
- Поиск операций по описанию без учёта регистра.
- Подсчёт количества операций, содержащих заданные категории в описании.

Установка

Клонируйте репозиторий и перейдите в папку проекта:

git clone https://github.com/Maryashka03/-Git.git
cd -Git

Установите зависимости:

pip install -r requirements.txt
pip install pytest flake8 isort

Использование

Запустите программу командой:

python -m src.main

Следуйте инструкциям в меню: выберите формат файла, укажите путь к нему и настройте фильтры.

Примеры функций

Поиск операций по описанию

from src.processing import process_bank_search

operations = [
    {"description": "Оплата в магазине"},
    {"description": "Перевод клиенту"},
]

result = process_bank_search(operations, "магазин")
print(result)

Подсчёт операций по категориям

from src.processing import process_bank_operations

operations = [
    {"description": "Оплата в магазине"},
    {"description": "Оплата в кафе"},
    {"description": "Перевод клиенту"},
]

result = process_bank_operations(
    operations,
    ["Оплата", "Перевод"],
)
print(result)

Проверка качества кода

Запуск тестов:

python -m pytest

Проверка покрытия тестами:

python -m pytest --cov=src --cov-report=term-missing

Проверка стиля кода:

python -m flake8 src tests

Проверка порядка импортов:

python -m isort --check-only src tests

Проверка типов (если установлен mypy):

python -m mypy src