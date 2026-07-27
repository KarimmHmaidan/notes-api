#!/bin/bash

echo "Waiting for database..."

while ! .venv/bin/python -c "
import psycopg2
from app.core.config import settings
psycopg2.connect(settings.database_url)
" ; do
  sleep 1
done

echo "Database is ready!"

echo "Running migrations..."
.venv/bin/alembic upgrade head

echo "Starting API..."
exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
