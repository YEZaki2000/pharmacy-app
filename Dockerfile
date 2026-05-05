# Gebruik Python 3.13 (of 3.11 als 3.13 problemen geeft)
FROM python:3.13-slim

# Set environment variabelen
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Werk directory
WORKDIR /app

# Installeer system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installeer Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Kopieer project
COPY . /app/

# Collect static files (voor productie)
RUN python manage.py collectstatic --noinput || true

# Expose poort
EXPOSE 8000

# Run migrations en start server
CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
