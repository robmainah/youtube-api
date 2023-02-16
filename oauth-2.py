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
    response = auth.videos().rate(rating='like', id='ArrNCcIXSIk').execute() # 137
    print(response)
    print("Successful")


def get_video_comments():
    request = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    response = request.commentThreads().list(
        part='snippet', videoId='jWh0FaRRZC4', maxResults=1
    ).execute()

    print(response['items'])


# auth = get_google_authorization()
# get_to_like_video(auth)
get_video_comments()
