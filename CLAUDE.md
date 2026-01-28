# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LPOJ (Lightweight Programming Online Judge) is a lightweight online judge system built with Django REST Framework (backend) and Vue.js (frontend). It supports multi-machine, multi-process judging with support for C/C++/Java/Python2/Python3/Swift5.1, Special Judge, and multiple choice questions. The system features class management and homework assignment functionality similar to LeetCode-style template problems.

**Key features:**
- Front-end/back-end separation for better performance
- Multi-machine, multi-process judging system
- Support for LeetCode-style template problem judging
- Class management and homework assignment features
- Real-time crawling of user blogs and submission counts from other OJ platforms
- Mobile-responsive design

## Architecture

The project is organized into 6 main modules:

1. **Frontend** (`/Frontend`) - Desktop web interface (Vue.js)
2. **FrontendMobile** (`/FrontendMobile`) - Mobile web interface (Vue.js)
3. **Backend** (`/Backend`) - REST API server (Django REST Framework)
4. **JudgerServer** (`/JudgerServer`) - Judging coordination server (Python)
5. **Judger** (`/Judger`) - Actual code judging engine (Python + C)
6. **CrawlingServer** (`/CrawlingServer`) - Crawls external OJ platforms for user data

### Backend Structure

The Backend is organized into Django apps, each handling a specific domain:
- `user/` - User authentication, profiles, and permissions
- `problem/` - Problem management and retrieval
- `judgestatus/` - Submission status tracking and results
- `contest/` - Contest/competition management
- `board/` - Discussion boards
- `blog/` - Blog system for users
- `wiki/` - Algorithm knowledge base
- `item/` - General item management
- `classes/` - Class management and homework assignments

All apps follow Django REST Framework patterns with `models.py`, `views.py`, `serializers.py`, and `urls.py`.

### Communication Flow

1. Users submit code through Frontend/FrontendMobile
2. Backend receives submissions and stores them in MySQL database
3. JudgerServer polls database for pending submissions
4. Judger instances connect to JudgerServer, download test data, and execute code
5. Judger reports results back to Backend via API
6. Frontend polls Backend for updated submission status

### Database

MySQL database named `LPOJ` stores all data. Database connection configured via environment variables:
- `DB_HOST` - Database host (default: localhost)
- `DB_USER` - Database user (default: root)
- `DB_PASSWORD` - Database password
- `DB_PORT` - Database port (default: 3306)

## Common Commands

### Docker Deployment (Recommended)

**Initial setup:**
```bash
# Clone and navigate to directory
git clone https://github.com/Linzecong/LPOJ.git && cd LPOJ

# Edit docker-compose.yml - MUST change all DB_PASSWORD and MYSQL_ROOT_PASSWORD fields
# Ensure ports 4406, 8080, 8000-8002, 9906 are available

# Start all services with 3 judger instances
sudo docker-compose up -d --scale judger=3

# Check all containers are running
sudo docker ps -a
```

**Update deployment:**
```bash
git pull
sudo docker-compose stop
sudo docker-compose pull
sudo docker-compose up -d --scale judger=3
```

**Custom build after code changes:**
```bash
# Edit docker-compose-build.yml with your database configuration
sudo docker-compose -f docker-compose-build.yml up -d --build --scale judger=3
```

### Backend Development

**With Docker:**
Backend runs on ports 8000-8002 (3 instances for load balancing)

**Without Docker:**
```bash
cd Backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py makemigrations judgestatus item problem user contest board blog wiki classes
python manage.py migrate

# Create superuser (admin/admin)
echo "from django.contrib.auth.models import User; User.objects.filter(email=\"admin@example.com\").delete(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin\")" | python manage.py shell

# Run development server
python manage.py runserver 0.0.0.0:8000

# For production, use gunicorn
gunicorn -w 5 --bind 0.0.0.0:8000 -k 'gevent' Backend.wsgi:application
```

### Frontend Development

**Desktop Frontend:**
```bash
cd Frontend
npm install
npm run dev     # Development server with hot reload
npm run build   # Production build to dist/
```

**Mobile Frontend:**
```bash
cd FrontendMobile
npm install
npm run dev     # Development server
npm run build   # Production build
```

### Judger Development

**Setup Judger:**
```bash
cd Judger

# Install dependencies
pip3 install -r requirements.txt

# Build the C judging core
cd JudgerCore
mkdir build && cd build
cmake ..
make

# Run judger
cd ../..
python3 main.py
```

### JudgerServer Development

```bash
cd JudgerServer

# Install dependencies
pip install -r requirements.txt

# Edit setting.json with database configuration
# Run server
sudo python main.py
```

### CrawlingServer Development

```bash
cd CrawlingServer
pip install -r requirements.txt
python main.py
```

## Configuration Files

- `docker-compose.yml` - Production deployment with pre-built images
- `docker-compose-build.yml` - Development deployment with local builds
- `Backend/Backend/settings.py` - Django settings including database configuration
- `Judger/setting.json` - Judger configuration (server IP, paths)
- `JudgerServer/setting.json` - JudgerServer configuration (database, port)

## Key Environment Variables

For Docker deployment, set these in docker-compose.yml:
- `DB_PASSWORD` - Database password (MUST change from default)
- `DB_HOST` - Database hostname
- `DB_USER` - Database username
- `DB_PORT` - Database port
- `SERVER_IP` - JudgerServer IP for Judger instances
- `BACKEND_IP` - Backend IP for Judgers to report results
- `NO_DOWNLOAD` - Set to "yes" to disable HTTP test data download
- `PYTHONSWF` - Set to "yes" to enable Python sensitive word filtering

## Initial Setup Checklist

After deployment:
1. Access OJ at `IP:8080` and register a user
2. Login to Django admin at `IP:8000/admin` (username: admin, password: admin)
3. Change admin password immediately
4. In User table, set your registered user's `type` field to `3` (super administrator)
5. Login as admin, navigate to admin page, submit settings once to initialize

## Testing

Tests are not currently implemented in this codebase. When adding tests, follow Django testing conventions for backend and Jest for frontend.

## Static Files

Static files (images for problems, etc.) should be placed in:
- `Frontend/dist/img/` for desktop
- `FrontendMobile/dist/img/` for mobile

These directories are mounted as volumes in Docker deployment.

## Port Reference

- `4406` - MySQL database
- `8000-8002` - Backend API servers (3 instances)
- `8080` - Frontend (desktop)
- `8081` - Frontend (mobile)
- `9906` - JudgerServer

## Documentation

Official documentation: https://docs.lpoj.cn
Demo site: https://oj.lpoj.cn
