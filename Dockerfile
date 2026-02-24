FROM python:3.11-slim

ENV POPPLER_PATH=/usr/bin

WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "-m", "app.main"]