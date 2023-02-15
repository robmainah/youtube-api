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


def get_channel_videos():
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    channelDetails = youtube.channels().list(
        id='UCkUq-s6z57uJFUFBvZIVTyg',
        part='contentDetails'
    ).execute()

    playlist_id = channelDetails['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while 1:
        response = youtube.playlistItems().list(
            playlistId=playlist_id, part='snippet', maxResults=50, pageToken=next_page_token
        ).execute()
        
        videos += response['items']
        next_page_token = response.get('nextPageToken')

        if next_page_token is None:
            break

    # for video in videos:
    #     print(video['snippet']['title'])
        
    return videos

def get_video_ids(videos):
    return list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))

def get_videos_stats(video_ids):
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))

    stats = []
    for i in range(0, len(video_ids), 50):
        response = youtube.videos().list(
            part='statistics', id=','.join(video_ids[i:i+50])
        ).execute()

        stats += response['items']

    return stats


def get_most_liked_video(stats):
    return sorted(stats, key=lambda x:int(x['statistics']['likeCount']), reverse=True)


# main()
videos = get_channel_videos()
video_ids = get_video_ids(videos)
statistics = get_videos_stats(video_ids)
most_liked_video = get_most_liked_video(statistics)
print(most_liked_video[0])
