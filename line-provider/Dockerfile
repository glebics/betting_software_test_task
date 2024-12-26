FROM python:3.10

WORKDIR /app

# Установка netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app/
COPY schemas.py /app/

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]
