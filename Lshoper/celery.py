import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "Lshoper.settings")
app = Celery('Lshoper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    "my_task_in_every_day": {
        "task": "cart.tasks.check_coupon_expire_date",
        "schedule": 60*60*24

    }

}
