"""
Django settings for windopen_starter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR: ", BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "keuhh=0*%do-ayvy*m2k=vss*$7)j8q!@u0+d^na7mi2(^!l!d"

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["watering.dev.qadre.io", "127.0.0.1", "localhost"]

ADMINS = [("Mihai", "mihai@qad.re")]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "windopen_app",
    "bootstrapform",
    "django_nose",
    "rest_framework",
    "corsheaders",
    # "rpyc_server",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "windopen_starter.urls"
# investigate how is this working
LOGIN_URL = "/windopen/login/"

WSGI_APPLICATION = "windopen_starter.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = "/static/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
        'APP_DIRS': True,
    },
]

# Use nose to run all tests
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# Tell nose to measure coverage on the "foo" and "bar" apps
NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=windopen/scripts",
]

CORS_ORIGIN_ALLOW_ALL = True

RPYC_PORT = 8010
# HOSTNAME = "watering.dev.qadre.io"
# HOSTNAME = "34.243.195.145"
HOSTNAME = "0.0.0.0"
# RPyc config
R_CONFIG = {
    "allow_pickle": True,
    "allow_getattr": True,
    "allow_setattr": True,
    "allow_delattr": True,
    "allow_all_attrs": True,
    }

SERVER_START = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s"
        },
        "verbose": {
            "format": "%(asctime)s %(levelname)-8s %(filename)s %(lineno)d %(message)s",
            "datefmt": "%y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
        "debugtoolbar": {
            "level": "DEBUG",
            "class": "logging.StreamHandler"
        },
        "windopen": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join("/var/log", "windopen", "windopen.log"),
            "maxBytes": 1024*1024,
            "backupCount": 5,
        },
        "mtu_service": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join("/var/log", "windopen", "mtu_service.log"),
            "maxBytes": 1024*1024,
            "backupCount": 5,
        }
    },
    "loggers": {
        "django": {
            "handlers": ["windopen"],
            "level": "DEBUG",
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "DEBUG",
        },
        "windopen": {
            "handlers": ["windopen"],
            "level": "DEBUG",
        },
        "mtu_service": {
            "handlers": ["mtu_service"],
            "level": "DEBUG",
        }
    }
}