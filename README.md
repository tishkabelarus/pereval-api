Pereval API
REST API для управления данными о горных перевалах.


для создания базы данных используйте python create_database.py из корневой папки проекта
для проверки таблиц базы данных используйте python check_tables.py из корневой папки проекта


 Описание


API позволяет добавлять и просматривать информацию о горных перевалах. При добавлении нового перевала автоматически устанавливается статус new.


Быстрый старт


1. Клонирование и настройка
bash

# Активация виртуального окружения
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt


2. Настройка окружения
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


Получение перевала


http
GET /pereval/{id}
Получение информации о перевале по ID.

Response:

json
{
    "status": 200,
    "message": "Success",
    "data": {
        "id": 1,
        "beautyTitle": "пер. ",
        "title": "Пхия",
        // ... полные данные перевала
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


Структура проекта


pereval_api/
├── app/
│   ├── models/database.py      # Работа с БД
│   ├── routes/pereval.py       # API endpoints
│   └── utils/validators.py     # Валидация данных
├── migrations/                 # SQL скрипты
├── pereval.db                 # База данных
├── requirements.txt           # Зависимости
├── run.py                    # Точка входа
└── .env                      # Переменные окружения
