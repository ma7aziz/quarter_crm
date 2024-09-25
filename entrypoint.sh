#!/bin/sh

# Wait for the PostgreSQL database to be ready
until pg_isready -h db -p 5432 -q; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Start the Django development server
exec "$@"
