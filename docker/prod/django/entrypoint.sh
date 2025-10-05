#!/bin/sh
set -e

echo "Starting Django application initialization..."

# Fix permissions on mounted volumes (run as root)
if [ "$(id -u)" = "0" ]; then
    echo "Fixing permissions on /app/static and /app/media..."
    chown -R django:fileserv /app/static /app/media 2>/dev/null || true
    chmod -R 770 /app/static /app/media 2>/dev/null || true
fi

# Wait for PostgreSQL to be ready using Python
echo "Waiting for PostgreSQL to be ready..."
python <<EOF
import time
import psycopg
import os

host = os.environ.get('SQL_HOST', 'db')
port = os.environ.get('SQL_PORT', '5432')
user = os.environ.get('SQL_USER', 'postgres')
password = os.environ.get('SQL_PASSWORD', 'postgres')
database = os.environ.get('SQL_DATABASE', 'postgres')

while True:
    try:
        conn = psycopg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=database,
            connect_timeout=1
        )
        conn.close()
        print("PostgreSQL is ready!")
        break
    except Exception:
        print(f"Waiting for PostgreSQL at {host}:{port}...")
        time.sleep(1)
EOF

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run quicksetup to create default users (idempotent - safe to run multiple times)
echo "Running quicksetup..."
python manage.py quicksetup

# Create superuser if environment variables are set and user doesn't exist
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Checking for superuser..."
    python <<EOF
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djdict.settings')
django.setup()

from dictionary.models import Author

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', f'{username}@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not Author.objects.filter(username=username).exists():
    Author.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        is_active=True
    )
    print(f'Superuser "{username}" created successfully!')
else:
    print(f'Superuser "{username}" already exists, skipping...')
EOF
fi

echo "Initialization complete! Starting application..."

# Execute the main command (gunicorn or celery)
# If running as root, switch to django user
if [ "$(id -u)" = "0" ]; then
    exec su-exec django "$@"
else
    exec "$@"
fi
