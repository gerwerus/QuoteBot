# QuoteBot

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
