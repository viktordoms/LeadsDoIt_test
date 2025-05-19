
import datetime
from celery import Celery
from libs.conf import CITY_WEATHER_SCHEDULE_HOUR

celery = Celery(
    'app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['libs.tasks.funcs']
)

celery.conf.timezone = 'UTC'

celery.conf.beat_schedule = {
    'fill_weather_history': {
        'task': 'libs.tasks.funcs.fill_weather_history',
        'schedule': datetime.timedelta(hours=int(CITY_WEATHER_SCHEDULE_HOUR)),
    },
}

