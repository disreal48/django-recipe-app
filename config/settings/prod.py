import environ
import os
import dj_database_url
from .base import *
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = env.str("CLOUD_NAME"), 
    api_key = env.str("API_KEY"), 
    api_secret = env.str("api_secret"),
    secure=True
)

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(str(BASE_DIR / ".env_prod"))

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")

MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE
INSTALLED_APPS = [
  'cloudinary_storage',
  'django.contrib.staticfiles',
  'cloudinary',
] + INSTALLED_APPS 

STATIC_ROOT = BASE_DIR / 'staticfiles'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env.str("CLOUD_NAME"),
    'API_KEY': env.str("API_KEY"),
    'API_SECRET': env.str("api_secret")
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


















db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)