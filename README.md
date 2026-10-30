Bank Widget — приложение для анализа банковских операций

Описание проекта

Учебное приложение для анализа банковских операций из Excel-файла.

Приложение позволяет:

- Загружать банковские операции из Excel.
- Формировать главную страницу с приветствием, информацией по картам и последними операциями.
- Получать курсы валют и цены акций через внешние API.
- Формировать страницу с расходами и доходами за выбранный период.
- Искать операции по описанию и категории.
- Формировать отчёт о расходах по выбранной категории за последние три месяца.
- Сохранять отчёты в CSV-файл.

Структура проекта

src/
    __init__.py
    main.py
    utils.py
    views.py
    external_api.py
    services.py
    reports.py

data/
    operations.xls

tests/
    test_utils.py
    test_views.py
    test_external_api.py
    test_services.py
    test_reports.py

user_settings.json
requirements.txt
README.md

Установка

Клонируйте репозиторий:

git clone https://github.com/Maryashka03/-Git.git
cd -Git

Установите зависимости:

pip install -r requirements.txt

Настройки

В файле "user_settings.json" можно указать необходимые валюты и акции:

{
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "MSFT", "GOOGL"]
}

Для получения курсов валют и цен акций используются API-ключи.

Создайте файл ".env" в корне проекта и добавьте:

EXCHANGE_RATES_API_KEY=ваш_ключ
ALPHA_VANTAGE_API_KEY=ваш_ключ

Без API-ключей приложение может запускаться, но данные о валютах и акциях не будут отображаться.

Запуск приложения

Из корневой папки проекта выполните:

python -m src.main

Проверка проекта

Запуск тестов:

python -m pytest -v

Проверка оформления кода:

python -m flake8 src tests

Проверка типов:

python -m mypy src

Используемые библиотеки

- pandas
- requests
- python-dotenv
- xlrd
- pytest
- flake8
- mypy