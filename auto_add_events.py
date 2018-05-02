
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetim
import json
import sys
import StringIO


def setup_calendar_api:
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

def build_json():
    for line in sys.stdin:
        event_data = line.strip().split(",")
        event_date,event_time,event_title,event_location = event_data

    print (event_time, event_title)

test_text = """18-05-10,6:00,Soccer Match,Oakridge HS Mini Field - West"""
def main():
	
	sys.stdin = StringIO.StringIO(test_text)
	build_json()
	sys.stdin = sys.__stdin__

main()
