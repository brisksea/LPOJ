FROM python:3.11-slim
LABEL maintainer="linzecong"
ADD . ./Backend
WORKDIR /Backend
ENV DB_HOST="lpojdatabase"
ENV DB_PASSWORD="lpojdatabase"
ENV DB_USER="root"
ENV DB_PORT=3306

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD python manage.py makemigrations && \
    python manage.py makemigrations judgestatus item problem user contest board blog wiki classes && \
    python manage.py migrate && \
    echo "from django.contrib.auth.models import User; User.objects.filter(email=\"admin@example.com\").delete(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin\")" | python manage.py shell && \
    gunicorn -w 5 --bind 0.0.0.0:8000 -k 'gevent' Backend.wsgi:application
