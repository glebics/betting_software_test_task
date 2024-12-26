#!/bin/sh

set -e

# Ожидание RabbitMQ
while ! nc -z rabbitmq 5672; do
  echo "Waiting for RabbitMQ..."
  sleep 1
done

# Ожидание PostgreSQL
while ! nc -z postgres_db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "RabbitMQ and PostgreSQL are up - starting bet_maker"

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000
