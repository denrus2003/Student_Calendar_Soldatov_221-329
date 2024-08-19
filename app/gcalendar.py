import datetime
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = '/Users/denis/Downloads/Учеба/Веб-технологии/student_calendar/service_account.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)
def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file('path/to/service_account.json')
    service = build('calendar', 'v3', credentials=creds)  # Fixed the import statement
    return service
def create_event(service, event_data):
    event = service.events().insert(calendarId='primary', body=event_data).execute()
    return event

def create_google_event(event):
    event = {
        'summary': event.title,
        'description': event.description,
        'start': {
            'dateTime': event.start_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': event.end_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event
