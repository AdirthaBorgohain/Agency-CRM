#!/bin/bash

set -e
  
# Function to check PostgreSQL availability using psycopg2
check_postgres() {
  python3 <<EOF
import os
import psycopg2
from psycopg2 import OperationalError
import time

# PostgreSQL connection parameters
db_host = os.environ.get("DB_HOST", "db")
db_user = os.environ.get("DB_USER", "postgres")
db_password = os.environ.get("DB_PASSWORD", "password")

while True:
    try:
        # Attempt to connect to PostgreSQL
        conn = psycopg2.connect(host=db_host, user=db_user, password=db_password)
        conn.close()
        print("Postgres is available")
        break
    except OperationalError:
        # Postgres is unavailable - sleep for 1 second and retry
        print("Postgres is unavailable - sleeping")
        time.sleep(1)

EOF
}

# Call the function to check PostgreSQL availability
check_postgres

echo "initializing django..."

# Apply migrations
python manage.py migrate

# Create superuser (if not exists)
if [ -z "$(python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists())")" ]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --no-input
fi

# Run Django development server
python manage.py runserver 0.0.0.0:8000