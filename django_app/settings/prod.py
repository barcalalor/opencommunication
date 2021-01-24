import dj_database_url


from django_app.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DEBUG=False
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)
CELERY_TIMEZONE = "Europe/Madrid"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60