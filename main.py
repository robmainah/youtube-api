from apiclient.discovery import build
from datetime import datetime
import environ

env = environ.Env()
environ.Env.read_env()

def main():
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))

    start_time = datetime(year=2005, month=1, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime(year=2008, month=2, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')

    request = youtube.search().list(
        q='python programming',
        type='video',
        part='snippet',
        maxResults=20,
        publishedAfter=start_time,
        publishedBefore=end_time
    )

    response = request.execute()
    items = response['items']

    for item in sorted(items, key=lambda x:x['snippet']['publishedAt']):
        # return print(item)
        print(item['snippet']['title'], item['snippet']['publishedAt'], item['id']['videoId'])



main()
