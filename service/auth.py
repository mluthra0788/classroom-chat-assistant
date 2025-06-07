from google_auth_oauthlib.flow import InstalledAppFlow

def get_credentials(scopes):
    flow = InstalledAppFlow.from_client_secrets_file("cred/user_cred.json", scopes)
    creds = flow.run_local_server(port=0)
    return creds
