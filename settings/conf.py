from decouple import config, Csv

BLOG_ENV_ID: str = config('BLOG_ENV_ID', default='local')
BLOG_SECRET_KEY: str = config('BLOG_SECRET_KEY')
BLOG_DEBUG: bool = config('BLOG_DEBUG', default=False, cast=bool)
BLOG_ALLOWED_HOSTS: list[str] = config('BLOG_ALLOWED_HOSTS', default='', cast=Csv())
BLOG_REDIS_URL: str = config('BLOG_REDIS_URL', default='redis://127.0.0.1:6379/1')