# API для расписания УГЛТУ

Базовый шаблон для проекта на FastAPI с использованием SQLAlchemy в качестве ORM и Alembic для миграций базы данных.

## 📦 Установка и настройка

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Создайте и активируйте виртуальное окружение (рекомендуется):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate    # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте переменные окружения:
   Создайте файл `.env` в корне проекта на основе `.env.example`:
   ```
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=username
    DB_PASSWORD=password
    DB_NAME=your_db_name
   ```

## 🚀 Запуск проекта

1. Запустите сервер FastAPI:
   ```bash
   python main.py
   ```

2. Откройте в браузере:
   - Документация Swagger: http://localhost:8000/docs
   - Документация ReDoc: http://localhost:8000/redoc

## 🛠 Миграции базы данных (Alembic)

1. Создание новой миграции:
   ```bash
   alembic revision --autogenerate -m "Your migration message"
   ```

2. Применение миграций:
   ```bash
   alembic upgrade head
   ```

3. Откат миграции:
   ```bash
   alembic downgrade -1
   ```

## 📂 Структура проекта

```
.
├── app/                       # Основное приложение
│   ├── api/                   # API эндпоинты
│   ├── core/                  # Основные настройки и конфиги
│   ├── models/                # SQLAlchemy модели
│   ├── schemas/               # Pydantic схемы
│   ├── services/              # Бизнес-логика
│   ├── main.py                # Точка входа в приложение
│   └── database.py            # Настройки базы данных
├── migrations/                # Миграции Alembic
├── tests/                     # Тесты
├── .env                       # Файл с переменными окружения
├── .env.example               # Пример файла .env
├── alembic.ini                # Конфиг Alembic
├── requirements.txt           # Зависимости
└── README.md                  # Этот файл
```

## 🧪 Тестирование

Для запуска тестов выполните:
```bash
pytest
```

