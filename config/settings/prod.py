import environ
import os
import dj_database_url
from .base import *
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1", "0.0.0.0"]
CSRF_TRUSTED_ORIGINS = [
    "https://localhost",
    "https://127.0.0.1",
    "https://0.0.0.0",
    "https://mysterious-brushlands-76647.herokuapp.com",
]

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(str(BASE_DIR / ".env_prod"))

# Configuration       
cloudinary.config( 
    cloud_name = env.str("CLOUD_NAME"), 
    api_key = env.str("API_KEY"), 
    api_secret = env.str("api_secret"),
    secure=True
)
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")

MIDDLEWARE = MIDDLEWARE + ["whitenoise.middleware.WhiteNoiseMiddleware"]
INSTALLED_APPS = [
  'cloudinary_storage',
  'django.contrib.staticfiles',
  'cloudinary',
] + INSTALLED_APPS 

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

STATIC_ROOT = BASE_DIR / 'staticfiles'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env.str("CLOUD_NAME"),
    'API_KEY': env.str("API_KEY"),
    'API_SECRET': env.str("api_secret")
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Configure Django App for Heroku.
import django_on_heroku
django_on_heroku.settings(locals())


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)