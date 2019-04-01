import os
# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
# Rpyc hostname
HOSTNAME = "0.0.0.0"

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.sqlite3',
        "NAME": os.path.join('/home/mihaido/Projects/windopen_v2/windopen/windopen_starter', 'db.sqlite3'),
    }
}
