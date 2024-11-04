# QuoteBot

## Описание проекта
Этот проект представляет собой систему автоматической генерации контента в Telegram. Администрирование происходит через телеграм бота.

## Запустить проект
```bash
docker-compose up --build --remove-orphans
```

## Локальная разработка (установка зависимостей)
```bash
poetry install
```

### Для локальной разработки последнюю строчку (scripts/webapp-entrypoint.sh)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Расположение виртуальных окружений
```
C:\Users\%username%\AppData\Local\pypoetry\Cache\virtualenvs
```