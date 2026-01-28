FROM node:18-slim

LABEL maintainer="linzecong"

# Install nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy pre-built frontend files from host
COPY Frontend/dist /frontend/dist
COPY Frontend/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
