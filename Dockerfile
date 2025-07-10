FROM python:3.12-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmagic-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install pip tools
RUN pip install --upgrade pip setuptools wheel

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app source
COPY . .

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
