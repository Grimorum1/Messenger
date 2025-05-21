# 💬 FastAPI Chat API

Асинхронный API для многопользовательского чата с поддержкой WebSocket, групп и истории сообщений.
Реализовано на FastAPI и SQLAlchemy с использованием PostgreSQL.

## Возможности

- 👤 Управление пользователями
- 👥 Создание групп и добавление пользователей
- 💬 Подключение к чату через WebSocket
- 🕘 История сообщений с пагинацией
- 🧹 Удаление сообщений по ID чата

## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy (Async)** — ORM для работы с БД
- **PostgreSQL** — база данных
- **WebSocket** — реалтайм соединение
- **Pydantic** — валидация данных
- **Docker** - контейнеризация
- **[UV](https://docs.astral.sh/uv/)** — пакетный менеджер  

## Клонирование и запуск

### 1. Клонируйте репозиторий

```bash
git clone git@github.com:Grimorum1/Messenger.git
cd Messenger
```

### 2. Запустите через docker compose

```bash
docker compose up 
```


## Swagger UI

Перейдите в браузере: `http://localhost:8000/docs`


## WebSocket подключение
Прежде чем подключиться к чату создайте его с помощью `POST` запроса - http://localhost:8000/chat/

Подключение к WebSocket чату:
```bash
ws://localhost:8000/chat/ws/{client_id}/{chat_id}
```
Пример:

```bash
ws://localhost:8000/chat/ws/1/5
```


## 👨‍💻 Автор
Прошу строго не судить, делалось максимально быстро, за пару дней. Всем добра)