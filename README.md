# Bank Widget

Учебный проект для обработки банковских операций клиента.

## Цель проекта

Проект содержит функции для фильтрации банковских операций по статусу
и сортировки операций по дате.

## Установка

Клонируйте репозиторий:

```bash
git clone <ссылка-на-ваш-репозиторий>
cd bankwidget
```

При необходимости установите инструменты проверки:

```bash
pip install pytest flake8 mypy isort
```

## Использование

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29"},
    {"id": 2, "state": "CANCELED", "date": "2018-09-12T21:27:25"},
]

print(filter_by_state(operations))
print(filter_by_state(operations, "CANCELED"))

print(sort_by_date(operations))
print(sort_by_date(operations, descending=False))
```

`filter_by_state` по умолчанию возвращает операции со статусом `EXECUTED`.

`sort_by_date` по умолчанию сортирует операции по убыванию даты,
то есть от самой новой к самой старой.

## Проверка

```bash
pytest
flake8 src tests
mypy src
isort --check-only src tests
```
