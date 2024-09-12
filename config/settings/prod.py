import environ
import os
import dj_database_url
from .base import *

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(str(BASE_DIR / ".env_prod"))

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")

MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE

STATIC_ROOT = BASE_DIR / 'staticfiles'



















db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)