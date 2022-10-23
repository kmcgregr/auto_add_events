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

    #TODO#############
    #  parse events.csv with format "Event description", "date", "time", "location"
    #  date parsing --- need to return start and end date in format yyyy-mm-day put it in a list
    #  tiime --- need to return start time and end time

    for line in lines:
        
        if line.find("Yard") != -1 or line.find("Garbage") != 0:
            event_data = line.strip().split(",")
            event_date,title = event_data
            time = "7:00 AM-7:00 AM"  
            location = "Redoak"
            description = "Garbage pickup"
        else:      
             event_data = line.strip().split(",")
             print (event_data)
             title,date,time,location,description = event_data
             event_date = str(build_date(date))
             print ("event date " + event_date)
        
        
        if time.find("-")!= -1:
            #split
            event_times = time.split('-')
            start_time,end_time = event_times
            event_start_time = str(convert24(start_time))
            event_end_time = str(convert24(end_time))
        else:
            event_start_time = str(convert24(time))
            event_end_time = event_start_time
                
        
        json_event = json.dumps(build_json(event_date,event_start_time.strip(),event_end_time.strip(),title,location,description))
        print (json_event)
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

    json_event_reminders = {}
    json_event_reminders['useDefault'] = 'True'

    json_event_data['reminders'] = json_event_reminders
    
    return json_event_data
    
def build_date(date_to_process):
    date_time_obj = datetime.datetime.strptime(date_to_process,"%d %B %Y")
    return date_time_obj.date()

def convert24(str1): 
      
    # Checking if last two elements of time 
    # is AM and first two elements are 12 
    if str1[-2:] == "AM" and str1[:1] == "12": 
        return "00" + str1[2:-2] 
          
    # remove the AM     
    elif str1[-2:] == "AM": 
        if int(stripcolon(str1[:2])) < 10:
            return '0' + str1[:-2] 
        else:
            return str1[:-2] 

    # Checking if last two elements of time 
    # is PM and first two elements are 12    
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
          
    else: 
          
        # add 12 to hours and remove PM 
        return str(int(str1[:1]) + 12) + ":" + str1[2:4] 

def stripcolon(str1):
    if str1.find(":") > 0 :
        return str1[:1]
    else:
        return str1


def main():
    with open('events.csv') as f:
        lines = f.readlines()

       
    calendar_service = setup_calendar_api()
    add_events_to_calender(calendar_service,lines)
    

main()
