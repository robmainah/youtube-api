from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import environ

env = environ.Env()
environ.Env.read_env()

def get_google_authorization():
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube']

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server()

    response = build('youtube', 'v3', credentials=credentials)

    print(response)
    return response


def get_to_like_video(auth):
    response = auth.videos().rate(rating='like', id='ArrNCcIXSIk').execute()
    print(response)
    print("Successful")


auth = get_google_authorization()
get_to_like_video(auth)
