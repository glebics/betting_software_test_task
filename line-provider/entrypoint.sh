#!/bin/sh

set -e

# Ожидание RabbitMQ
while ! nc -z rabbitmq 5672; do
  echo "Waiting for RabbitMQ..."
  sleep 1
done

echo "RabbitMQ is up - starting line_provider"

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000
