import time
from Lshoper.celery import app
from celery import shared_task
from Lshoper.celery import app
from account.models import Otp


@shared_task
def delete_expire_code(username):
    time.sleep(3*60)
    Otp.objects.get(username=username).delete()




