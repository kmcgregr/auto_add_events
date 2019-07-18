import datetime
import sys

def process_dates(lines_data):
    print(lines_data)
    for line in lines_data:
        event_data = line.strip().split(",")
        description,date,time,location,notes = event_data
        #print(description)
        #build_date(date)
        build_time(time)
        #print(location)

def build_date(date_to_process):
    date_time_obj = datetime.datetime.strptime(date_to_process,"%d %B %Y")
    return date_time_obj.date()

def build_time(time_to_process):
    event_times = time_to_process.split('-')
    start_time,end_time = event_times
    print(convert24(start_time))
    print(convert24(end_time))
    #print(convert24(start_end_date))
    

def convert24(str1): 
      
    # Checking if last two elements of time 
    # is AM and first two elements are 12 
    if str1[-2:] == "AM" and str1[:1] == "12": 
        return "00" + str1[2:-2] 
          
    # remove the AM     
    elif str1[-2:] == "AM": 
        return '0' + str1[:-2] 
      
    # Checking if last two elements of time 
    # is PM and first two elements are 12    
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
          
    else: 
          
        # add 12 to hours and remove PM 
        return str(int(str1[:1]) + 12) + ":" + str1[2:4] 


def main():
    with open('events.csv') as f:
        lines = f.readlines()
  
    process_dates(lines)
    

main()