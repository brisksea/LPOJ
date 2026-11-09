FROM python:3.11-slim
LABEL maintainer="linzecong"
ADD . ./CrawlingServer
WORKDIR /CrawlingServer

# Install system dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
