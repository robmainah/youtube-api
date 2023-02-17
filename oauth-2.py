import os
import pickle
import environ
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

env = environ.Env()
environ.Env.read_env()


def save_credentials_to_pickle(credentials, file_name):
    file = open(file_name, "ab")
    pickle.dump(credentials, file)
    file.close()


def get_auth_credentials_from_pickle():
    file = open("client_secret.pickle", "rb")
    credentials = pickle.load(file)
    file.close()
    return credentials


def get_google_authorization():
    file_name = "client_secret.pickle"

    if os.path.exists(file_name):
        return
    
    CLIENT_SECRET_FILE = "client_secret.json"
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server()

    response = build("youtube", "v3", credentials=credentials)

    save_credentials_to_pickle(response, file_name)

    print(response)
    return response


def like_a_video():
    auth = get_auth_credentials_from_pickle()
    response = auth.videos().rate(rating="like", id="ArrNCcIXSIk").execute()  # 137
    print("Successful")


def get_video_comments():
    request = build("youtube", "v3", developerKey=env("YOUTUBE_API_KEY"))
    results = (
        request.commentThreads()
        .list(part="snippet", videoId="jWh0FaRRZC4", maxResults=1)
        .execute()
    )

    print(results)


def get_video_comments_by_search_term():
    request = build("youtube", "v3", developerKey=env("YOUTUBE_API_KEY"))
    results = (
        request.commentThreads()
        .list(part="snippet", videoId="jWh0FaRRZC4", searchTerms="linux")
        .execute()
    )

    # print(results['items'][1:len(results['items'])]) # without first items
    # print(results['items'][-1:]) # get last item
    # print(results['items'][:1]) # get first item
    print(results)


def comment_on_video(auth):
    request = auth.commentThreads().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                videoId="jWh0FaRRZC4",
                topLevelComment=dict(
                    snippet=dict(textOriginal="I just love the video")
                ),
            )
        ),
    )
    response = request.execute()

    print(response)


# def save_google_authentication(auth):
# create pickle file to save auth


# auth = get_google_authorization()
get_google_authorization()
like_a_video()
# get_video_comments()
# get_video_comments_by_search_term()
# comment_on_video(auth)
# save_google_authentication()
