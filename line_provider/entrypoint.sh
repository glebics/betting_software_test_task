#!/bin/sh

set -e

# Если переданы аргументы (например, pytest), выполните их
if [ "$1" = "pytest" ]; then
    exec "$@"
fi

# Ожидание RabbitMQ
while ! nc -z rabbitmq 5672; do
  echo "Waiting for RabbitMQ..."
  sleep 1
done

echo "RabbitMQ is up - starting line_provider"

# Запуск приложения
exec uvicorn main:app --host 0.0.0.0 --port 8000