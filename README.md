Pereval API
REST API для управления данными о горных перевалах.


для создания базы данных используйте python create_database.py из корневой папки проекта
для проверки таблиц базы данных используйте python check_tables.py из корневой папки проекта


 Описание


API позволяет добавлять и просматривать информацию о горных перевалах. При добавлении нового перевала автоматически устанавливается статус new.


Быстрый старт


1 Клонирование и настройка
bash

Активация виртуального окружения
venv\Scripts\activate

 Установка зависимостей
pip install -r requirements.txt


2 Настройка окружения
Создайте файл .env в корне проекта:

env
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=postgres
FSTR_DB_PASS=password
FSTR_DB_NAME=pereval

HOST=0.0.0.0
PORT=8000
DEBUG=True

3. Инициализация базы данных
bash
python create_database.py

4. Запуск приложения
bash
python run.py
Приложение будет доступно по адресу: http://localhost:8000


API Endpoints


Health Check
http
GET /health
Проверка работоспособности сервера.

Response:

json
{
    "status": "ok"
}

Получение перевала по ID
```http
GET /submitData/{id}

Добавление перевала


http
POST /submitData


Добавление нового перевала в базу данных.


Request Body:

json
{
    "beautyTitle": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "user": {
        "email": "user@email.tld",
        "phone": "79031234567",
        "fam": "Пупкин",
        "name": "Василий",
        "otc": "Иванович"
    },
    "coords": {
        "latitude": "45.3842",
        "longitude": "7.1525",
        "height": "1200"
    },
    "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
    },
    "images": {
        "images": [
            {"title": "Седловина", "file_path": "/images/1.jpg"},
            {"title": "Подъем", "file_path": "/images/2.jpg"}
        ]
    },
    "activities": [1, 2]
}
Response:

json
{
    "status": 200,
    "message": "Success",
    "id": 1
}



Редактирование перевала
http
PATCH /submitData/{id}

Request Body:

Response:

json
{
    "state": 1,
    "message": "Success"
}
или

json
{
    "state": 0,
    "message": "Error message"
}


Получение перевалов пользователя
http
GET /submitData/?user__email={email}

Response:

json
{
    "status": 200,
    "message": "Success",
    "data": [
        {
            "id": 1,
            "title": "Пхия",
            "beautyTitle": "пер. ",
            "status": "new",
            "date_added": "2024-01-01 12:00:00"
        }
    ]
}

Получение перевала


http
GET /pereval/{id}



json
Получение полной информации о перевале по его ID.

Response:

json
{
    "status": 200,
    "message": "Success",
    "data": {
        "id": 1,
        "beautyTitle": "пер. ",
        "title": "Пхия",
        "other_titles": "Триев",
        "connect": "",
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"
        },
        "user": {
            "email": "user@email.tld",
            "phone": "79031234567",
            "fam": "Пупкин",
            "name": "Василий",
            "otc": "Иванович"
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        },
        "status": "new",
        "images": [...],
        "activities": [...]
    }
}


Структура базы данных


users - пользователи

perevals - перевалы (статус: new, accepted, rejected)

pereval_images - изображения перевалов

spr_activities_types - типы активностей

pereval_activities - связь перевалов и активностей


Технические детали


Фреймворк: Flask

База данных: SQLite

Аутентификация: Отсутствует (для разработки)

Кодировка: UTF-8




 Тестирование
Проект имеет полное покрытие тестами с использованием pytest.

Запуск тестов
bash
# Установите тестовые зависимости если еще не установлены
pip install pytest

# Запуск всех тестов
pytest tests/

# Запуск с подробным выводом
pytest tests/ -v

# Запуск тестов с покрытием кода
pytest --cov=app tests/

# Запуск конкретного файла тестов
pytest tests/test_database.py
pytest tests/test_correct.py





Структура проекта


pereval_api/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py          # DatabaseManager class
│   ├── routes/
│   │   ├── __init__.py
│   │   └── pereval.py           # API endpoints
│   └── utils/
│       ├── __init__.py
│       └── validators.py        # Data validation
├── tests/
│   ├── __init__.py
│   ├── test_correct.py          # API integration tests
│   └── test_database.py         # DatabaseManager unit tests
├── migrations/
│   └── init_tables.sql          # SQL initialization script
├── pereval.db                   # SQLite database
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── create_database.py           # Database initialization
├── check_tables.py              # Database structure check
├── .env.example                 # Environment variables template
└── pytest.ini    