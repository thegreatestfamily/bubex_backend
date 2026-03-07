# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for OpenCV and FFmpeg
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Make build script executable
RUN chmod +x /app/build.sh

# The build script will be run by Render, or we can use CMD for manual Docker runs
CMD ["gunicorn", "bubex_core.wsgi:application", "--bind", "0.0.0.0:8000"]
