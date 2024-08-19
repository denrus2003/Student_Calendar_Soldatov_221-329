import caldav
from caldav.elements import dav, cdav
from datetime import datetime, timedelta
from flask import current_app

def get_calendar_client():
    client = caldav.DAVClient(
        url=current_app.config['CALDAV_URL'],
        username=current_app.config['CALDAV_USERNAME'],
        password=current_app.config['CALDAV_PASSWORD']
    )
    return client

def get_calendars():
    client = get_calendar_client()
    principal = client.principal()
    calendars = principal.calendars()
    return calendars

def create_event(summary, start, end, description=''):
    calendars = get_calendars()
    calendar = calendars[0]  # Выберите нужный календарь

    event = calendar.add_event(
        f"""
        BEGIN:VCALENDAR
        VERSION:2.0
        BEGIN:VEVENT
        UID:{datetime.now().timestamp()}
        DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
        DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}
        DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}
        SUMMARY:{summary}
        DESCRIPTION:{description}
        END:VEVENT
        END:VCALENDAR
        """
    )
    return event