import dj_database_url


from django_app.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DEBUG=False
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)