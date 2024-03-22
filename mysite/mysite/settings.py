import io
import os
from pathlib import Path
from urllib.parse import urlparse

import environ
import google.auth
from google.cloud import secretmanager

# project directory
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env.devlkjdlkasdf")


try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass


if os.path.isfile(env_file):
    env.read_env(env_file)
elif os.getenv("TRAMPOLINE_CI", None):
    placeholder = (
        f"SECRET_KEY=a\n"
        "GS_BUCKET_NAME=None\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
    env.read_env(io.StringIO(placeholder))
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # load environment variables from secret manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")


# CSRF
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    # settings for cloud run
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main_app.apps.MainAppConfig",
    "django_bootstrap5",
    "widget_tweaks",
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


ROOT_URLCONF = "mysite.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(path.parent) for path in BASE_DIR.glob("**/templates/**/*.html")],
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


WSGI_APPLICATION = "mysite.wsgi.application"


# database connection
DATABASES = {"default": env.db_url("DJANGO_DATABASE_URL")}
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    # settings for cloud sql auth proxy
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432


AUTH_USER_MODEL = "main_app.Respondents"


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


LANGUAGE_CODE = "ja"
TIME_ZONE = "Japan"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# file storage
# media can be path specified by location, but static must be STATIC_URL
STATIC_URL = "static/"
STORAGES = {
    # media
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": "test_media_storage",
            "default_acl": "publicRead",
            "querystring_auth": False,
            "location": "",
        },
    },
    # static
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": env("DJANGO_STATIC_FILES_BUCKET_NAME"),
            "default_acl": "publicRead",
            "querystring_auth": False,
        },
    },
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
