# Import the Secret Manager client library.
from google.cloud import secretmanager
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

def get_secret(secret_id):
    try:
        project_id = os.environ.get('PROJECT_NAME')
        if not project_id:
            raise ValueError("PROJECT_NAME environment variable is not set")

        client = secretmanager.SecretManagerServiceClient()
        parent = f"projects/{project_id}"
        secret_name = f"{parent}/secrets/{secret_id}/versions/latest"

        response = client.access_secret_version(request={"name": secret_name})
        payload = response.payload.data.decode("UTF-8")
        return payload
    except Exception as e:
        logging.error(f"Failed to get secret {secret_id}: {e}")
        raise

def get_id_token():
    try:
        keyString = get_secret('invoker_key')
        key_dict = json.loads(keyString)
        audience = os.environ.get('BACKLOG_URL')
        if not audience:
            raise ValueError("BACKLOG_URL environment variable is not set")

        credentials = service_account.IDTokenCredentials.from_service_account_info(
            key_dict, 
            target_audience=audience
        )
        request = Request()
        credentials.refresh(request)
        identity_token = credentials.token
        return identity_token
    except Exception as e:
        logging.error(f"Failed to get ID token: {e}")
        raise

