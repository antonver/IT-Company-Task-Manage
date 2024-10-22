from dotenv import load_dotenv
import dj_database_url

from .base import *




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ["it-company-task-manage-1.onrender.com", "127.0.0.1"]



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('POSTGRES_DB'),
    'USER': os.getenv('POSTGRES_USER'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'HOST': os.getenv('POSTGRES_HOST'),
    'PORT': os.getenv('POSTGRES_DB_PORT', 5432),
    'OPTIONS': {
      'sslmode': 'require',
    },
  }
}
