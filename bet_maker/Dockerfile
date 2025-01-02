# bet_maker/Dockerfile
FROM python:3.10

WORKDIR /app/bet_maker

# Установка netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей и установка
COPY requirements.txt /app/bet_maker/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . /app/bet_maker/

# Копирование тестов
# COPY tests /app/tests/ интеграционные тесты запускаются отдельно

# Копирование скрипта запуска
COPY entrypoint.sh /app/bet_maker/
RUN chmod +x /app/bet_maker/entrypoint.sh

CMD ["./entrypoint.sh"]
