# Blog API — Homework 4 (Nginx Reverse Proxy)

## 📌 Overview
This homework extends HW3 by adding **Nginx as a reverse proxy** in front of the Django application.  
All services run via Docker Compose on localhost.

---

## 🏗 Architecture


Browser / curl
│
http://localhost

▼
Nginx (port 80)
│
proxy_pass → web:8000
▼
Daphne (Django ASGI)


Other services:
- Redis (cache, broker, channels)
- Celery worker & beat
- Flower (monitoring)

---

## ⚙️ Setup & Run

### 1. Build and start all services
```bash
docker compose up --build
2. Stop services
docker compose down
🌐 Services
Service	URL
API	http://localhost/api/

Admin	http://localhost/admin/

Swagger	http://localhost/api/docs/

ReDoc	http://localhost/api/redoc/

Flower	http://localhost:5555
🔧 Nginx Features
Reverse proxy to Django (web:8000)
Serves static files from /static/
Serves media files from /media/
Supports WebSockets (/ws/)
Adds required proxy headers
Caches static files (30 days)
📁 Static & Media
Static files served from: /var/www/static
Media files served from: /var/www/media
Django does NOT serve static files (DEBUG=False)
🔌 WebSocket Support

Endpoint:

ws://localhost/ws/posts/<slug>/comments/?token=<jwt>
Uses Upgrade and Connection headers
Returns 101 Switching Protocols
Real-time comment updates
✅ Verification Steps
1. Nginx is working
curl -I http://localhost/admin/login/

Expected:

HTTP/1.1 200 OK
Server: nginx/...
2. Static files served by nginx
curl -I http://localhost/static/admin/css/base.css

Expected:

Cache-Control: max-age=...
3. API works
curl http://localhost/api/posts/

Expected: JSON response

4. Port 8000 is NOT accessible
curl http://localhost:8000/

Expected:

connection refused
5. Nginx returns 502 if backend is down
docker compose stop web
curl -I http://localhost/api/posts/

Expected:

502 Bad Gateway
6. WebSocket works
wscat -c "ws://localhost/ws/posts/<slug>/comments/?token=<jwt>"

Expected:

101 Switching Protocols
🔐 Environment Variables

Defined in:

settings/.env

Example:

BLOG_REDIS_URL=redis://redis:6379/0
BLOG_CELERY_BROKER_URL=redis://redis:6379/1
BLOG_FLOWER_USER=admin
BLOG_FLOWER_PASSWORD=changeme
📌 Important Notes
Only Nginx (port 80) is exposed to host
Django (port 8000) is internal only
Static & media served by Nginx
DEBUG=False in Docker environment
🏁 Result

The project now:

Uses Nginx as reverse proxy
Supports WebSockets through proxy
Serves static/media efficiently
Runs fully in Docker with one command
