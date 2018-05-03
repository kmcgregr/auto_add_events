
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import json
import sys
import StringIO

MY_TIMEZONE = "America/New_York"

def setup_calendar_api():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service

def add_events_to_calender(service):

    for line in sys.stdin:
        event_data = line.strip().split(",")
        event_date,event_start_time,event_end_time,event_title,event_location = event_data
    json_event = json.dumps(build_json(event_date,event_start_time,event_end_time,event_title,event_location))
    event = service.events().insert(calendarId='primary', body=json_event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

def build_json(event_date,event_start_time,event_end_time,event_title,event_location):
  
    json_event_data = {}
    

    json_start_date = {}
    json_start_date['timeZone'] = MY_TIMEZONE
    json_start_date['dateTime'] = event_date + "T" + event_start_time
    
    json_event_data['start'] = json_start_date

    json_end_date = {}
    json_end_date['dateTime'] = event_date + "T" + event_end_time
    json_end_date['timeZone'] = MY_TIMEZONE
   
    json_event_data['end'] = json_end_date

    json_event_data['summary'] = event_title
    json_event_data['location'] = event_location
    return json_event_data

test_text = """2018-05-10,18:00,19:00,Soccer Match,Oakridge HS Mini Field - West"""

def main():
    sys.stdin = StringIO.StringIO(test_text)
    calender_service = setup_calendar_api()
    add_events_to_calender(calender_service)
    sys.stdin = sys.__stdin__

main()
