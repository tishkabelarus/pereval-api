-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    fam VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    otc VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица областей
CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY,
    id_parent INTEGER NOT NULL,
    title TEXT NOT NULL
);

-- Таблица перевалов
CREATE TABLE IF NOT EXISTS perevals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    beauty_title VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    other_titles VARCHAR(255),
    connect TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    height INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    area_id INTEGER DEFAULT 1,
    level_winter VARCHAR(10),
    level_summer VARCHAR(10),
    level_autumn VARCHAR(10),
    level_spring VARCHAR(10),
    status VARCHAR(20) DEFAULT 'new',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (area_id) REFERENCES areas(id)
);

-- Таблица изображений
CREATE TABLE IF NOT EXISTS pereval_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pereval_id INTEGER NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255),
    file_path VARCHAR(500) NOT NULL,
    FOREIGN KEY (pereval_id) REFERENCES perevals(id) ON DELETE CASCADE
);

-- Таблица типов активностей
CREATE TABLE IF NOT EXISTS spr_activities_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

-- Связующая таблица перевалов и активностей
CREATE TABLE IF NOT EXISTS pereval_activities (
    pereval_id INTEGER NOT NULL,
    activity_type_id INTEGER NOT NULL,
    PRIMARY KEY (pereval_id, activity_type_id),
    FOREIGN KEY (pereval_id) REFERENCES perevals(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_type_id) REFERENCES spr_activities_types(id)
);

-- Вставка начальных данных
INSERT OR IGNORE INTO areas (id, id_parent, title) VALUES
(1, 0, 'Памиро-Алай'),
(65, 0, 'Алтай'),
(66, 65, 'Северо-Чуйский хребет');

INSERT OR IGNORE INTO spr_activities_types (id, title) VALUES
(1, 'пешком'),
(2, 'лыжи'),
(3, 'катамаран'),
(4, 'байдарка'),
(5, 'плот'),
(6, 'сплав'),
(7, 'велосипед'),
(8, 'автомобиль'),
(9, 'мотоцикл'),
(10, 'парус'),
(11, 'верхом');