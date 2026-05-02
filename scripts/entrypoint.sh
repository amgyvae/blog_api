#!/usr/bin/env sh
set -e

echo "Waiting for Redis..."
until python - <<'PY'
import os, sys
import redis
url = os.getenv("BLOG_REDIS_URL", "")
if not url:
    print("BLOG_REDIS_URL is missing")
    sys.exit(1)
r = redis.Redis.from_url(url)
r.ping()
print("Redis is ready")
PY
do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Compiling translations..."
python manage.py compilemessages || true

if [ "${BLOG_SEED_DB}" = "true" ]; then
  echo "Seeding DB..."
  python manage.py seed || true
fi

echo "Starting command: $@"
exec "$@"