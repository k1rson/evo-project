import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evo.settings')

app = Celery('evo')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-user-activity': {
        'task': 'api.v1.api_chat_app.tasks.check_user_activity',
        'schedule': 10.0
    }
}
