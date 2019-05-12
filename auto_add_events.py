from __future__ import print_function
import datetime
import json
import pickle
import sys
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

MY_TIMEZONE = "America/New_York"
TIME_FILLER = ":00"

def setup_calendar_api():
     
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
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
    
    json_start_date['dateTime'] = event_date + 'T' + event_start_time + TIME_FILLER
    json_start_date['timeZone'] = MY_TIMEZONE
    json_event_data['start'] = json_start_date 

    json_end_date = {}
    json_end_date['dateTime'] = event_date + 'T' + event_end_time + TIME_FILLER
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
