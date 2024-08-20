import requests
import os ;
import services.utilities.sercret_service as secret 

def say_hello():

    return "MenkaIX"

def getRoot():
    
    url = os.environ.get('BACKLOG_URL')

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + secret.get_id_token()
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text
