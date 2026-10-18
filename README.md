# Bank Widget

Учебный проект для обработки банковских операций.

## Возможности

* Фильтрация банковских операций по статусу.
* Сортировка операций по дате.
* Загрузка списка операций из JSON-файла.
* Конвертация сумм транзакций в рубли.

## Установка

Установите зависимости:

   bash
pip install requests python-dotenv pytest flake8 mypy isort


## Загрузка операций из JSON

Функция `load_transactions` из `src/utils.py` загружает данные из JSON-файла. Если файл отсутствует, содержит некорректный JSON или данные не являются списком словарей, функция возвращает пустой список.

Пример:

   python
from src.utils import load_transactions

operations = load_transactions("data/operations.json")
print(operations)


## Конвертация валют

Функция `convert_to_rub` из `src/external_api.py` возвращает сумму транзакции в рублях. Для USD и EUR используется API обменных курсов.

Для настройки создайте файл `.env` в корне проекта и добавьте API-ключ:

   text
EXCHANGE_RATES_API_KEY=ваш_api_ключ


Шаблон переменных окружения находится в `.env.example`. Не публикуйте настоящий API-ключ и не добавляйте файл `.env` в Git.

Пример вызова:

   python
from src.external_api import convert_to_rub

transaction = {
    "operationAmount": {
        "amount": "1500",
        "currency": {"code": "RUB"}
    }
}

print(convert_to_rub(transaction))


## Проверка проекта

Запуск тестов:

   bash
python -m pytest -q


Проверка оформления кода:

   bash
python -m flake8 src tests