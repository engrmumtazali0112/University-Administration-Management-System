"""
Django settings for hostel_management_system (Vercel + Neon ready).
All secrets come from environment variables - never hard-code them.
"""
import os
from pathlib import Path

import dj_database_url

try:  # local development only; Vercel injects env vars itself
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- Core
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [".vercel.app", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_select2",

    "hostel",
]

# Cloudinary media storage (enabled only when CLOUDINARY_URL is set)
USE_CLOUDINARY = bool(os.environ.get("CLOUDINARY_URL"))
if USE_CLOUDINARY:
    INSTALLED_APPS.insert(INSTALLED_APPS.index("django.contrib.staticfiles"), "cloudinary_storage")
    INSTALLED_APPS.append("cloudinary")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hostel_management_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hostel_management_system.wsgi.application"

# ---------------------------------------------------------------- Database
# Uses Neon Postgres when DATABASE_URL is set, otherwise local SQLite.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=0,  # serverless + Neon pooler: don't keep connections open
        ssl_require=bool(os.environ.get("DATABASE_URL")),
    )
}

# ---------------------------------------------------------------- Auth
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------- i18n
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------- Static & media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if USE_CLOUDINARY
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------- Email (Gmail SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("SMTP_PORT", 587))
EMAIL_HOST_USER = os.environ.get("SMTP_USERNAME", "")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_FROM", EMAIL_HOST_USER)
EMAIL_TO = os.environ.get("EMAIL_TO", EMAIL_HOST_USER)

# ---------------------------------------------------------------- Stripe (if used)
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")

# ---------------------------------------------------------------- Security (production)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True