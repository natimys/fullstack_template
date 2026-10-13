# 🏛️ Fullstack Template
Template для Fullstack приложений на базе FastAPI + React.js

## 💫 Стек технологий
Backend:
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- asyncpg

Frontend:
- React.js
- Tailwind CSS
- Next.js

## Локальный запуск

1. Скопируйте шаблон окружения и задайте уникальные `DB_PASSWORD` и `JWT_SECURITY_KEY` (не менее 32 символов для ключа):

   ```bash
   cp .env.example .env
   # заполнить необходимые переменные
   docker compose up -d --build
   ```

   Python и Node.js на хосте устанавливать не нужно. PostgreSQL доступен только внутри Compose; миграции выполняются backend entrypoint перед запуском API.
2. Создайте первого администратора внутри backend-контейнера: `docker compose exec backend python -m core.admin create --email admin@example.com --name Administrator`. Команда запросит пароль в скрытом вводе.
3. Откройте frontend на `http://localhost:3000`. Браузер ходит к `/api` на том же origin; Next.js перенаправляет запросы backend внутри Compose.

Для HTTPS за reverse proxy задайте `JWT_COOKIE_SECURE=true`. CLI разработчика запускается на хосте через `uv run ft`; `ft module`, `ft db`, `ft doctor`, `ft test` и `ft dev` доступны из корня проекта.

## Production

Разворачивайте Compose за reverse proxy с HTTPS. В `.env` задайте уникальные случайные `DB_PASSWORD` и `JWT_SECURITY_KEY` (например, `openssl rand -hex 32`), `DEBUG=false`, `JWT_COOKIE_SECURE=true` и точный публичный origin в `CORS_ORIGINS` (например, `https://example.com`). Порты frontend и backend привязаны только к `127.0.0.1`; proxy должен передавать внешний HTTPS трафик на frontend. База данных не публикует порт.

## 👩‍💻 Добавление новых модулей
Через CLI добавьте новый модуль
