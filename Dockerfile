FROM python:3.12-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

COPY wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x wait-for-postgres.sh

COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

