"""
Django settings for CreeDictionary project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import logging
import os
import posixpath
from pathlib import Path
from sys import stderr

from .coerce import to_boolean
from .hostutils import HOST_IS_SAPIR, HOSTNAME

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "72bcb9a0-d71c-4d51-8694-6bbec435ab34"

# sapir.artsrn.ualberta.ca has some... special requirements,
# so let's hear about it!
RUNNING_ON_SAPIR = to_boolean(os.environ.get("RUNNING_ON_SAPIR", HOST_IS_SAPIR))

# Debug is default to False
# Turn it to True in development
DEBUG = to_boolean(os.environ.get("DEBUG", False))

# SECURITY WARNING: don't run with debug turned on in production!
if RUNNING_ON_SAPIR:  # pragma: no cover
    assert not DEBUG

# GitHub Actions and other services set CI to `true`
CI = to_boolean(os.environ.get("CI", False))

# The Django debug toolbar is a great help when... you know... debugging Django,
# but it has a few issues:
#  - the middleware SIGNIFICANTLY increases request times
#  - the debug toolbar adds junk on the DOM, which may interfere with end-to-end tests
#
# The reasonable default is to enable it on development machines and let the developer
# opt out of it, if needed.
if "ENABLE_DJANGO_DEBUG_TOOLBAR" in os.environ:
    ENABLE_DJANGO_DEBUG_TOOLBAR = to_boolean(os.environ["ENABLE_DJANGO_DEBUG_TOOLBAR"])
else:
    ENABLE_DJANGO_DEBUG_TOOLBAR = DEBUG

# The debug toolbar should ALWAYS be turned off:
#  - when DEBUG is disabled
#  - in CI environments
if not DEBUG or CI:
    ENABLE_DJANGO_DEBUG_TOOLBAR = False


# Host settings:

if DEBUG:
    ALLOWED_HOSTS = ["*"]
elif RUNNING_ON_SAPIR:  # pragma: no cover
    ALLOWED_HOSTS = ["sapir.artsrn.ualberta.ca"]
else:  # pragma: no cover
    ALLOWED_HOSTS = [HOSTNAME, "localhost"]

# Application definition

INSTALLED_APPS = [
    # Add your apps here to enable them
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "API.apps.APIConfig",
    "CreeDictionary.apps.CreeDictionaryConfig",
    "morphodict.apps.MorphodictConfig",
    "django_js_reverse",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "securemiddleware.set_secure_headers",
]

# configure tools for development, CI, and production
if DEBUG and ENABLE_DJANGO_DEBUG_TOOLBAR:
    # enable django-debug-toolbar for development
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(
        0, "debug_toolbar.middleware.DebugToolbarMiddleware"
    )  # middleware order is important

    # works with django-debug-toolbar app
    DEBUG_TOOLBAR_CONFIG = {
        # Toolbar options
        "SHOW_COLLAPSED": True,  # collapse the toolbar by default
    }

    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "CreeDictionary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # 'threaded': True,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "CreeDictionary.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# if this is set, use existing test database
USE_TEST_DB = to_boolean(os.environ.get("USE_TEST_DB", False))


if USE_TEST_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

############################### Morphodict configuration ###############################

MORPHODICT_SOURCES = [
    {
        "abbrv": "MD",
        "title": "Maskwacîs Dictionary of Cree Words / Nehiyaw Pîkiskweninisa",
        "editor": "Maskwaschees Cultural College",
        "publisher": "Maskwachees Cultural College",
        "year": 2009,
        "city": "Maskwacîs, Alberta",
    },
    {
        "abbrv": "CW",
        "title": "nêhiyawêwin : itwêwina / Cree : Words",
        "editor": "Arok Wolvengrey",
        "year": 2001,
        "publisher": "Canadian Plains Research Center",
        "city": "Regina, Saskatchewan",
    },
    {
        "abbrv": "AE",
        "title": "Alberta Elders' Cree Dictionary/"
        "alperta ohci kehtehayak nehiyaw otwestamâkewasinahikan",
        "author": "Nancy LeClaire, George Cardinal",
        "editor": "Earle H. Waugh",
        "year": 2002,
        "publisher": "The University of Alberta Press",
        "city": "Edmonton, Alberta",
    },
]

# The ISO 639-1 code is used in the lang="" attributes in HTML.
MORPHODICT_ISO_639_1_CODE = "cr"

# What orthographies -- writing systems -- are available
# Plains Cree has two primary orthographies:
#  - standard Roman orthography (e.g., nêhiyawêwin)
#  - syllabics (e.g., ᓀᐦᐃᔭᐍᐏᐣ)
#
# There may be further sub-variants of each orthography.
#
# Morphodict assumes that the `text` of all Wordform are written in the default
# orthography.
MORPHODICT_ORTHOGRAPHY = {
    # All entries in Wordform should be written in SRO (êîôâ)
    "default": "Latn",
    "available": {
        # 'Latn' is Okimāsis/Wolvegrey's SRO
        "Latn": {"name": "SRO (êîôâ)"},
        "Latn-x-macron": {
            "name": "SRO (ēīōā)",
            "converter": "CreeDictionary.orthography.to_macrons",
        },
        "Cans": {
            "name": "Syllabics",
            "converter": "CreeDictionary.orthography.to_syllabics",
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

############################## API app settings ###############################

# We only apply affix search for user queries longer than the threshold length
AFFIX_SEARCH_THRESHOLD = 4

############################## staticfiles app ###############################

if RUNNING_ON_SAPIR:  # pragma: no cover
    # on sapir /cree-dictionary/ is used to identify the service of the app
    # XXX: this is kind of a hack :/
    STATIC_URL = "/cree-dictionary/static/"
else:
    STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

if DEBUG:
    # Use the default static storage backed for debug purposes.
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    # In production, use a manifest to encourage aggressive caching
    # Note requires `python manage.py collectstatic`!
    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    # learn how different loggers are used in Django: https://docs.djangoproject.com/en/3.0/topics/logging/#id3
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
