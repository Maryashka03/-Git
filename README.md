# Bank Widget

Учебный проект для обработки банковских операций клиента.

## Цель проекта

Проект содержит функции для фильтрации банковских операций по статусу,
сортировки операций по дате и обработки транзакций с помощью генераторов.

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

### Обработка операций

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

### Генераторы

Модуль `generators` содержит функции для обработки большого количества
транзакций с помощью генераторов и итераторов.

#### Фильтрация транзакций по валюте

Функция `filter_by_currency` возвращает транзакции только с указанной валютой.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")

for transaction in usd_transactions:
    print(transaction)
```

#### Получение описаний транзакций

Функция `transaction_descriptions` поочерёдно возвращает описание каждой
транзакции.

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)

for description in descriptions:
    print(description)
```

#### Генерация номеров банковских карт

Функция `card_number_generator` генерирует номера банковских карт в формате
`XXXX XXXX XXXX XXXX` в заданном диапазоне.

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```

Результат:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```

## Проверка
### Логирование выполнения функций

Модуль `decorators` содержит декоратор `log`, который записывает информацию о выполнении функций.

Декоратор поддерживает два режима работы:

* Если аргумент `filename` не указан, сообщения выводятся в консоль.
* Если указан `filename`, сообщения записываются в соответствующий файл.

При успешном выполнении функции записывается её имя и сообщение `ok`. Если возникает ошибка, записываются имя функции, тип ошибки и входные аргументы.

Пример использования:

```python
from src.decorators import log

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
```

При успешном выполнении в лог записывается:

```text
my_function ok
```

При возникновении ошибки, например, при делении на ноль:

```text
my_function error: ZeroDivisionError. Inputs: (1, 0), {}
```

Для проверки декоратора используются тесты `pytest`, которые проверяют успешное выполнение функций, запись логов в файл и консоль, а также обработку ошибок.

```bash
pytest
python -m pytest --cov=src --cov-report=html
flake8 src tests
mypy src
isort --check-only src tests
```

HTML-отчёт о покрытии тестами создаётся в папке `htmlcov`.