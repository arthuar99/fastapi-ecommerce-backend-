# Use official Python runtime as a parent image
FROM python:3.12-slim

# Set workdir
WORKDIR /usr/src/app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Use uvicorn to run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
