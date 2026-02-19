#!/bin/bash
set -e

echo "=============================="
echo "Running database migrations..."
echo "=============================="

# Cek apakah flask command tersedia (Flask-Migrate)
if command -v flask >/dev/null 2>&1; then
    echo "Flask detected, running migrations..."
    flask db upgrade
else
    echo "No flask command found, skipping migrations."
fi

echo "=============================="
echo "Starting Gunicorn..."
echo "=============================="

# Jalankan Gunicorn
exec gunicorn --bind 0.0.0.0:8000 run:app --workers 2
