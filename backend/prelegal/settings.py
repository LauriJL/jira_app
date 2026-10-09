"""Django settings for the PreLegal backend."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Repository root (contains the shared "templates" directory).
REPO_ROOT = BASE_DIR.parent

SECRET_KEY = "django-insecure-dev-key-change-me-in-production"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "corsheaders",
    "nda",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "prelegal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "prelegal.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The React dev server and the built app may call the API from another origin.
CORS_ALLOW_ALL_ORIGINS = True

# Directory holding the Common Paper markdown templates (see task PL-4).
COMMON_PAPER_TEMPLATES_DIR = REPO_ROOT / "templates"
