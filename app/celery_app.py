from celery import Celery
from celery.schedules import crontab

from app.config import settings

app = Celery(
    'app',
    broker=settings.get_connection_rabbit(),
    include=['app.tasks']
)

app.conf.beat_schedule = {
    'check-servers-every-minute': {
        'task': 'app.tasks.check_servers',
        'schedule': crontab(minute='*/1'),
    },
}
