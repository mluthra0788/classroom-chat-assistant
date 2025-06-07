import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def get_credentials(scopes):
    flow = InstalledAppFlow.from_client_secrets_file(r"C:\Users\Dell\PycharmProjects\classroom-chat-assistant\service\client_secret.json", scopes)
    creds = flow.run_local_server(port=0)
    return creds
