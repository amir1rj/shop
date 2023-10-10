from datetime import datetime

from celery import app, shared_task
from django.utils.timezone import now

from products.models import CouponCode

def diffNowDate(DateStr):
   fmt = '%Y-%m-%d'
   d2 = datetime.strptime(str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day), fmt)
   d1 = datetime.strptime(DateStr, fmt)
   return (d2-d1).days
@shared_task
def check_coupon_expire_date():
    codes =CouponCode.objects.all()
    for code in codes:
        if code.expire:
            if diffNowDate(str(code.expire))<=0:
                code.delete()