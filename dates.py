from datetime import datetime
from datetime import timedelta


def end_date():
    end_date = datetime.now() 
    return end_date
def start_date():
    start_date = end_date - timedelta(days=14)
    return start_date