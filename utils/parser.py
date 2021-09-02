from datetime import datetime, timedelta

def parse_date(date: datetime):
    return date.strftime("%I:%M %p %A, %B %d, %Y")

def parse_seconds(sec):
    return timedelta(seconds=sec)