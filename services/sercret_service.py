# Import the Secret Manager client library.
from google.cloud import secretmanager
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import json
import os


def get_secret(secret_id):

    
    project_id = os.environ.get('PROJECT_NAME')

    client = secretmanager.SecretManagerServiceClient()

    parent = f"projects/{project_id}"


    # Build the secret name.
    secret_name = f"{parent}/secrets/{secret_id}/versions/latest"

    # Access the secret version.
    response = client.access_secret_version(request={"name": secret_name})

    payload = response.payload.data.decode("UTF-8")
    
    return payload

def get_id_token():

    keyString = get_secret('invoker_key')

    key_dict = json.loads(keyString)

    # Specify the audience for the identity token
    audience = os.environ.get('BACKLOG_URL') #""

    # Load the service account credentials from the dictionary
    credentials = service_account.IDTokenCredentials.from_service_account_info(
        key_dict, 
        target_audience=audience
    )

    # Create a request object
    request = Request()

    # Refresh the credentials to obtain an identity token
    credentials.refresh(request)

    # Get the identity token
    identity_token = credentials.token

    return identity_token

def say_hello():

    return "MenkaIX"