# line_provider/Dockerfile
FROM python:3.10

WORKDIR /app/line_provider

# Установка netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей и установка
COPY requirements.txt /app/line_provider/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . /app/line_provider/

# Копирование тестов
# COPY tests /app/line_provider/tests/ интеграционные тесты запускаются отдельно

# Копирование скрипта запуска
COPY entrypoint.sh /app/line_provider/
RUN chmod +x /app/line_provider/entrypoint.sh

CMD ["./entrypoint.sh"]
