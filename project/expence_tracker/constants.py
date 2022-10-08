import pytz
from datetime import datetime
from django.utils import timezone
from pytz import timezone as pytztimezone
def prepare_date_time(date, date_time_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    try:
        return pytz.utc.localize(datetime.strptime(date, date_time_format))
    except:
        raise Exception("Dates are not in proper format")

SELECT_CATEGORY_CHOICES = [
    ("Food","Food"),
    ("Travel","Travel"),
    ("Shopping","Shopping"),
    ("Necessities","Necessities"),
    ("Entertainment","Entertainment"),
    ("Other","Other")
 ]