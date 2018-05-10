
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
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
    
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow,store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service

def add_events_to_calender(service, lines):

    for line in lines:
        event_data = line.strip().split(",")
       
        event_date,event_start_time,event_end_time,event_title,event_location,event_description = event_data
       
        json_event = json.dumps(build_json(event_date,event_start_time,event_end_time,event_title,event_location,event_description))
       
        calendar_events = json.loads(json_event)
       
        event = service.events().insert(calendarId='primary', body=calendar_events).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

def build_json(event_date,event_start_time,event_end_time,event_title,event_location,event_description):
  
    json_event_data = {}
    

    json_start_date = {}
    
    json_start_date['dateTime'] = event_date + 'T' + event_start_time
    json_start_date['timeZone'] = MY_TIMEZONE
    json_event_data['start'] = json_start_date

    json_end_date = {}
    json_end_date['dateTime'] = event_date + 'T' + event_end_time
    json_end_date['timeZone'] = MY_TIMEZONE
   
    json_event_data['end'] = json_end_date
    
    json_event_data['location'] = event_location
    json_event_data['summary'] = event_title
    json_event_data['description'] = event_description
    
    return json_event_data
    


def main():
    with open('events.csv') as f:
        lines = f.readlines()

       
    calender_service = setup_calendar_api()
    add_events_to_calender(calender_service,lines)
    

main()
