import requests
import time
from datetime import datetime
global auth_cookie

TIMEKEEPER_URL = "http://cyber.cs.du.edu/timekeeper/"
TIME_API_URL = "http://cyber.cs.du.edu/timekeeper/api/v1/time"


def get_auth_cookie():
    response = requests.get(TIMEKEEPER_URL)
    cookies = response.cookies.get_dict()
    return cookies.get("_acdk")


def format_time(data):
    dt = datetime(
        year=data["year"],
        month=data["month"],
        day=data["day"],
        hour=data["hour"],
        minute=data["minute"],
        second=data["second"]
    )

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_current_time(auth_cookie):
    while True:
        try:
            response = requests.get(TIME_API_URL, cookies={"_acdk": auth_cookie})
            date_str = response.headers['Date']
            date_time = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_time = date_time.strftime("%Y-%m-%d %H:%M")
            print(formatted_time)
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    auth_cookie = get_auth_cookie()

    if auth_cookie:
        print(f"Auth Cookie: {auth_cookie}")
        get_current_time(auth_cookie)

    else:
        print("Failed to get auth cookie")
