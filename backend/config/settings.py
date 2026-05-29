"""
Django settings for config project.
"""

from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

def env_bool(name, default=False):
    raw = str(config(name, default=str(default))).strip().lower()
    if raw in {"1", "true", "yes", "y", "on"}:
        return True
    if raw in {"0", "false", "no", "n", "off"}:
        return False
    return default


SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me")
DEBUG = env_bool("DEBUG", default=True)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="127.0.0.1,localhost,testserver")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shop.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True

# Static and media readiness (collectstatic + uploaded media).
STATIC_URL = "static/"
STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = PROJECT_DIR / "media"

# Store profile from environment.
STORE_PROFILE = {
    "name": config("STORE_NAME", default="Kazplants"),
    "whatsapp_phone": config("WHATSAPP_PHONE", default="77757560046"),
    "instagram_url": config("INSTAGRAM_URL", default="https://instagram.com/kazplants"),
    "phone": config("STORE_PHONE", default="+7 775 756 00 46"),
    "address": config("STORE_ADDRESS", default="Астана, Казахстан"),
}

WHATSAPP_PHONE = STORE_PROFILE["whatsapp_phone"]

# Production readiness toggles.
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", default=not DEBUG)
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", default=not DEBUG)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", cast=int, default=0 if DEBUG else 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=not DEBUG)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", default=not DEBUG)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": config("LOG_LEVEL", default="INFO"),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
