FROM node:18-slim

LABEL maintainer="linzecong"

# Install nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy pre-built mobile frontend files from host
COPY FrontendMobile/dist /frontend/dist
COPY FrontendMobile/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
