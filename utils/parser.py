from datetime import datetime

def parse_date(date: datetime):
    return date.strftime("%I:%M %p %A, %B %d, %Y")