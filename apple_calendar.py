import requests
from datetime import datetime, timedelta
from flask import current_app
from requests.auth import HTTPBasicAuth

def get_calendar_client():
    # Используем requests для соединения с сервером
    return {
        'url': current_app.config['CALDAV_URL'],
        'username': current_app.config['CALDAV_USERNAME'],
        'password': current_app.config['CALDAV_PASSWORD']
    }

def get_calendars():
    client = get_calendar_client()
    response = requests.request(
        "PROPFIND",
        client['url'],
        auth=HTTPBasicAuth(client['username'], client['password']),
        headers={
            "Depth": "1",
            "Content-Type": "application/xml"
        },
        data="""<?xml version="1.0" encoding="utf-8" ?>
            <D:propfind xmlns:D="DAV:">
                <D:prop>
                    <D:displayname />
                    <D:resourcetype />
                </D:prop>
            </D:propfind>"""
    )
    if response.status_code == 207:
        # Вернуть список найденных календарей
        return response.content
    else:
        raise Exception(f"Failed to fetch calendars. Status: {response.status_code}")

def create_event(summary, start, end, description=''):
    client = get_calendar_client()
    calendar_url = f"{client['url']}/calendars/your_calendar_id/"  
    event_uid = datetime.now().timestamp()

    event_data = f"""
    BEGIN:VCALENDAR
    VERSION:2.0
    BEGIN:VEVENT
    UID:{event_uid}
    DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
    DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}
    DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}
    SUMMARY:{summary}
    DESCRIPTION:{description}
    END:VEVENT
    END:VCALENDAR
    """

    response = requests.request(
        "PUT",
        f"{calendar_url}{event_uid}.ics",
        auth=HTTPBasicAuth(client['username'], client['password']),
        headers={
            "Content-Type": "text/calendar"
        },
        data=event_data
    )

    if response.status_code in [200, 201]:
        print("Event created successfully.")
    else:
        raise Exception(f"Failed to create event. Status: {response.status_code}")
