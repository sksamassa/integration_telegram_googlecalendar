import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def book_timeslot(event_description, booking_time, input_email, booking_date=None):
    """Books a time slot in the Google Calendar."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    if not booking_date:
        booking_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    start_time = f"{booking_date}T{booking_time}:00+05:00"
    end_time = f"{booking_date}T{int(booking_time[:2])+1}:00:00+05:00"

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    if not events:
        event = {
                        'summary': 'Hair Cut Appointment',
            'location': 'Cheliabinsk',
            'description': f"{event_description} with AutomationFeed",
            'start': {
                'dateTime': start_time,
                'timeZone': 'Asia/Yekaterinburg',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Asia/Yekaterinburg',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                {'email': 'sksamassa@gmail.com'},
                {'email': input_email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created:', event.get('htmlLink'))
        return True
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            if start == start_time:
                print('Already booked.')
                return False

        event = {
            'summary': 'Event Appointment',
            'location': 'Cheliabinsk',
            'description': f"{event_description} with AutomationFeed",
            'start': {
                'dateTime': start_time,
                'timeZone': 'Asia/Yekaterinburg',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Asia/Yekaterinburg',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                {'email': 'sksamasssa@gmail.com'},
                {'email': input_email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created:', event.get('htmlLink'))
        return True

if __name__ == '__main__': 
    result = book_timeslot(event_description, booking_time, input_email)
