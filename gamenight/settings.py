"""Django settings for gamenight project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import logging
import os
from pathlib import Path

import sentry_sdk

if SENTRY_DSN := os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )
else:
    logging.warning("No SENTRY_DSN set, not enabling sentry")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA, HOST = os.environ.get("HOST", "http://localhost").split("://", 1)
PORT = os.environ.get("PORT", "8000")

SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-key")
FERNET_KEY = os.environ.get("FERNET_KEY", "fffffffffffffffffffffffffffffffffffffffffff=")

DEBUG = os.environ.get("DEBUG", "1") == "1"

ALLOWED_HOSTS: list[str] = [
    HOST,
]
CSRF_TRUSTED_ORIGINS = [f"{SCHEMA}://{host}" for host in ALLOWED_HOSTS]


INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "gamenight.games",
    "django_tables2",
    "django_filters",
    "iommi",
    "django_extensions",
]

MIDDLEWARE = [
    "iommi.live_edit.Middleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "gamenight.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "iommi.sql_trace.Middleware",
    "iommi.profiling.Middleware",
    "iommi.middleware",
]

ROOT_URLCONF = "gamenight.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "gamenight" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "gamenight.wsgi.application"
ASGI_APPLICATION = "gamenight.asgi.application"
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {  # type: ignore[var-annotated]
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "CONN_MAX_AGE": 5,
        "CONN_HEALTH_CHECKS": True,
        "NAME": os.environ.get("PGDATABASE", "gamenight"),
        "USER": os.environ.get("PGUSER", "gamenight"),
        "PASSWORD": os.environ.get("PGPASSWORD", "gamenight"),
        "PORT": os.environ.get("PGPORT", "5432"),
        "HOST": os.environ.get("PGHOST", "localhost"),
        "OPTIONS": {},
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "games.User"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/users/"

PUBLIC_PATHS = [
    "/auth/login/",
    "/games/",
    "/users/",
    "/users/login/token/*",
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

IOMMI_DEFAULT_STYLE = "bootstrap5p"
