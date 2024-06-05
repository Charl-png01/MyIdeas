from datetime import datetime
from requests import Session
from time import sleep

# Defining the base and endpoint URLs
endpoint = "http://cyber.cs.du.edu/timekeeper"
api_endpoint = "/api/v1/time"
session = Session()

# Establishing a session and retrieving the token
initial_response = session.get(endpoint)
page_content = initial_response.text
token_indicator = '__window_token = "'
token_start_index = page_content.find(token_indicator) + len(token_indicator)
token_end_index = page_content.find('"', token_start_index)
session_token = page_content[token_start_index:token_end_index]

# Headers for subsequent requests
request_headers = {
    "Authorization": "Bearer " + session_token,
    "X-TimeKeeper-Channel": "Web"
}

# Constructing the full API URL
full_api_url = endpoint + api_endpoint

# Loop to continuously fetch and display the time
try:
    while True:
        api_response = session.get(full_api_url, headers=request_headers)
        if api_response.status_code == 200:
            time_data = api_response.json()
            formatted_datetime = datetime(
                year=time_data['year'],
                month=time_data['month'],
                day=time_data['day'],
                hour=time_data['hour'],
                minute=time_data['minute'],
                second=time_data['second'],
                microsecond=time_data['microsecond']
            ).strftime("%Y-%m-%d %H:%M:%S")
            print(formatted_datetime)
            sleep(5)  # Wait for 3 seconds
        else:
            print(f"Error fetching time: {api_response.text}")
except KeyboardInterrupt:
    print("Process terminated by user.")

