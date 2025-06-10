import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

NOVATER_API_URL = os.getenv('API_URL')
NOVATER_USERNAME = os.getenv('API_USERNAME')
NOVATER_PASSWORD = os.getenv('API_PASSWORD')

def fetch_current_schedule():
    """This function fetches data from the api, inserts a datetime object into the data and returns that data in json format.
    In case of error fetching data function returns None"""
    try:
        response = requests.get(
            NOVATER_API_URL,
            auth=HTTPBasicAuth(NOVATER_USERNAME, NOVATER_PASSWORD)
        )
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Converting expires date string to datetime object for easier comparison
        expires_date_str = data.get('expires', {}).get('date')
        if expires_date_str:
            # Inserting datetime object into pricesheet
            data['expires']['date_obj'] = datetime.strptime(expires_date_str, "%Y-%m-%d %H:%M:%S.%f")

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching schedule: {e}")
        return None
    
