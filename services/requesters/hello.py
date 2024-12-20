import requests
import os ;
import services.utilities.sercret_service as secret 
import logging

logging.basicConfig(level=logging.INFO)

def say_hello():

    return "MenkaIX"

def getRoot():
    try:
        url = os.environ.get('BACKLOG_URL')
        if not url:
            raise ValueError("BACKLOG_URL environment variable is not set")

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + secret.get_id_token()
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
        return "An error occurred while fetching the root."
    except Exception as e:
        logging.error(f"Failed to get root: {e}")
        return "An unexpected error occurred."
