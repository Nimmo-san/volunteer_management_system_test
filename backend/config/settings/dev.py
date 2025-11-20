
from .base import *  # noqa: F403


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173"
# ]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_CREDENTIALS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}