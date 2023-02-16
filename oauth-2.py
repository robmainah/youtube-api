from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def get_google_authorization():
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube']

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server()
    
    youtube = build('youtube', 'v3', credentials=credentials)

    print(youtube)

get_google_authorization()
