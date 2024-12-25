FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app/
COPY db.py /app/
COPY models.py /app/
COPY schemas.py /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
