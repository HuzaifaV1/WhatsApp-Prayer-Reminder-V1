import requests  # Import the requests library to make HTTP requests 
import schedule  # Import the schedule library for scheduling tasks
import time      # Import the time library for adding delay
import pywhatkit # Import the pywhatkit library for sending WhatsApp messages


def sendmessage(message):
    # Function that sends a WhatsApp message to multiple people
    pywhatkit.sendwhatmsg_to_group_instantly("GROUP_ID", message, 15, tab_close=True)
    pywhatkit.sendwhatmsg_instantly('PHONE_NUMBER', message, 15, tab_close=True)
    pywhatkit.sendwhatmsg_instantly('PHONE_NUMBER', message, 15, tab_close=True)    
    pywhatkit.sendwhatmsg_instantly('PHONE_NUMBER', message, 15, tab_close=True)        
    pywhatkit.sendwhatmsg_instantly('PHONE_NUMBER', message, 15, tab_close=True)

while True:
    # Make a GET request to the prayer timings API
    response = requests.get('http://api.aladhan.com/v1/timingsByCity?city=Regina&country=Canada&method=2')
    if response.status_code == 200:
        # If the request to the API was successful, extract the prayer timings
        prayer_information = response.json()['data']['timings']            
        
        # Create a list of tuples which contain the prayer names and timings 
        prayer = list(zip(prayer_information.keys(), prayer_information.values()))
        # Filter out unnecessary data
        prayer = [t for t in prayer if t[0] != 'Imsak' and t[0] != 'Firstthird' and t[0] != 'Lastthird' and t[0] != 'Midnight' and t[0] != 'Sunset']
        # Creates a formatted table of prayer timings 
        table = '```--------------------\n| Prayer  | Time   |\n| --------|--------|\n'
        for p in prayer:
            table += f'| {p[0]:<7} | {p[1]:>6} |\n'
        table += '--------------------```'
        print(table)
        # Schedule a WhatsApp message for each prayer
        for p in prayer:            
            schedule.every().day.at(p[1]).do(sendmessage, f'*Time to pray {p[0]}* \n {table}')            
        
        # Run all the scheduled tasks and add a delay of 30 seconds 
        while True:
            schedule.run_pending()
            time.sleep(30)
        
    else:
        # If the request fails pring status code and response reason
        print(f'Error: {response.status_code} - {response.reason}')
        time.sleep(60)
        
