"""
Django settings for the civic_reporter project.

This is a development-friendly config (sqlite db, DEBUG=True).
Before deploying, move SECRET_KEY / DEBUG / ALLOWED_HOSTS into
environment variables (python-decouple is already in requirements.txt
for this) and switch to a real database.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security -----------------------------------------------------------
SECRET_KEY = "dev-only-secret-key-change-me"  # TODO: load from env before prod
DEBUG = True
ALLOWED_HOSTS = ["*"]  # TODO: restrict in production

# --- Apps -----------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party
    "rest_framework",
    "rest_framework_simplejwt",

    # local apps (App1_accounts, App2_reports, ... from the class diagram)
    "accounts",
    "reports",
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

ROOT_URLCONF = "civic_reporter.urls"

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

WSGI_APPLICATION = "civic_reporter.wsgi.application"
ASGI_APPLICATION = "civic_reporter.asgi.application"

# --- Database (sqlite for dev; swap for Postgres in production) ---------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Custom user model (accounts.User, see accounts/models.py) ----------
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n -----------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

# --- Static / media ---------------------------------------------------
STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"  # before_image / after_image uploads land here

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Django REST Framework ----------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# --- SimpleJWT ------------------------------------------------------------
from datetime import timedelta  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}
