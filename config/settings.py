import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

SITE_ID = int(os.getenv("DJANGO_SITE_ID"))

LOGIN_URL = "/admin/login/"
LOGOUT_REDIRECT_URL = "/"


# Application definition

INSTALLED_APPS = [
    "admin_reorder",
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "mentions",
    "admin",
    "content",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    "mentions.middleware.WebmentionHeadMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [
                "utilities.taglibrary",
                "django.contrib.humanize.templatetags.humanize",
                "django.templatetags.static",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data/sqlite/db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    "config.auth.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/assets/"
STATIC_ROOT = BASE_DIR / "assets/static"
STATICFILES_DIRS = [BASE_DIR / "build"]


# Media root for uploads
# https://docs.djangoproject.com/en/dev/topics/files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "assets/media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Caching...
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
        "TIMEOUT": 300,
        "OPTIONS": {"MAX_ENTRIES": 500},
    }
}


# Webmentions...
DOMAIN_NAME = os.getenv("DJANGO_DOMAIN")
WEBMENTIONS_USE_CELERY = False
WEBMENTIONS_ALLOW_OUTGOING_DEFAULT = True
WEBMENTIONS_DOMAINS_OUTGOING_DENY = [
    "*.wikipedia.org",
    "daringfireball.net",
    "github.com",
    "hachyderm.io",
    "hbr.org",
    "indieweb.social",
    "kottke.org",
    "mastodon.online",
    "mastodon.social",
    "medium.com",
    "mstdn.social",
    "news.ycombinator.com",
    "sentiers.media",
    "techhub.social",
    "wired.com",
    "xoxo.zone",
    "youtu.be",
    "*.youtube.com",
]

WEBMENTIONS_DOMAINS_OUTGOING_TAG_DENY: str = "wm-nosend"

# Admin interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Admin reorder
ADMIN_REORDER = (
    {
        "app": "content",
        "label": "Content",
        "models": ("content.Content",),
    },
    {
        "app": "mentions",
        "label": "Webmentions",
        "models": (
            {
                "model": "mentions.Webmention",
                "label": "Incoming webmentions",
            },
            {
                "model": "mentions.PendingIncomingWebmention",
                "label": "Pending incoming webmentions",
            },
            {
                "model": "mentions.OutgoingWebmentionStatus",
                "label": "Outgoing webmentions",
            },
            {
                "model": "mentions.PendingOutgoingContent",
                "label": "Pending outgoing webmentions",
            },
            "mentions.SimpleMention",
            "mentions.HCard",
        ),
    },
    {
        "app": "auth",
        "label": "Administration",
        "models": (
            "auth.User",
            "auth.Group",
            "sites.Site",
            "admin_interface.Theme",
        ),
    },
)


# CSP directives
CSP_INCLUDE_NONCE_IN = [
    "script-src",
    "style-src",
]
CSP_DEFAULT_SRC = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
CSP_FRAME_ANCESTORS = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",)
CSP_IMG_SRC = (
    "'self'",
    "'unsafe-inline'",
    "data:",
    "https:",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "nonce",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "nonce",
)
CSP_WORKER_SRC = (
    "'self'",
    "blob:",
)
CSP_CONNECT_SRC = (
    "'self'",
    "https:",
)
CSP_FRAME_SRC = (
    "'self'",
    "https://www.youtube.com",
    "https://youtu.be",
)
CSP_BASE_URI = ("'none'",)
