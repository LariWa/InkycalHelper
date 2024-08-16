import requests
from requests.auth import HTTPBasicAuth
import time
# Define the URL and local file path
url = "http://ds218.local/caldav/calendar/home/"
local_file_path = "/home/pi/Documents/calendar.ics"
username = 'calendar'
password = 'syncWithRaspi'

while True:
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    # Check if the request was successful
    if response.status_code == 200:
        # Save the file content to a local file
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
    else:
        print(f'Failed to download file. Status code: {response.status_code}')
     # Wait for 10 minutes
    time.sleep(600) 