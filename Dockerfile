# Base Python image
FROM python:3.12-slim

# Work directory
WORKDIR /app

# Avoid Python buffering logs
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port Fly.io uses
EXPOSE 8000

# Start server with Gunicorn
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
