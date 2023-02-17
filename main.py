from apiclient.discovery import build
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import environ

env = environ.Env()
environ.Env.read_env()

def main():
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))

    # start_time = datetime(year=2005, month=1, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
    # end_time = datetime(year=2008, month=2, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')

    request = youtube.search().list(
        q='matiangi foreign interview -citizen',
        type='video',
        part='snippet',
        maxResults=20,
        # publishedAfter=start_time,
        # publishedBefore=end_time
    )

    response = request.execute()
    items = response['items']

    for item in sorted(items, key=lambda x:x['snippet']['publishedAt']):
        # return print(item)
        print(item['snippet']['title'], item['snippet']['publishedAt'], item['id']['videoId'])


def get_channel_videos(channel_id, part='id,snippet', limit=10):
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    channelDetails = youtube.channels().list(
                    id=channel_id, part='contentDetails').execute()

    playlist_id = channelDetails['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while 1:
        response = youtube.playlistItems().list(
            playlistId=playlist_id, part=part, maxResults=min(limit, 50),
            pageToken=next_page_token).execute()
        
        videos += response['items']
        next_page_token = response.get('nextPageToken')

        if next_page_token is None or len(videos) >= limit:
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
    items = sorted(stats, key=lambda x:int(x['statistics']['likeCount']), reverse=True)
    print(items[0])


def get_channel(channel_name):
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    results = youtube.search().list(
        part='id, snippet', q=channel_name, type='channel_name'
    ).execute()

    return results['items'][0]


def parse_publish_timestamp(video):
    # return datetime.fromisoformat(video['snippet']['publishedAt']) + timedelta(hours=1, minutes=0)
    return datetime.fromisoformat(video['snippet']['publishedAt'])


def plot_graph(publish_times):
    plt.hist(publish_times, bins=24)
    plt.xticks(range(24))
    plt.show()


main()
# videos = get_channel_videos('UC-lHJZR3Gqxm24_Vd_AJ5Yw')
# video_ids = get_video_ids(videos)
# statistics = get_videos_stats(video_ids)
# most_liked_video = get_most_liked_video(statistics)

# channel_id = get_channel('t-series')['id']['channelId']
# videos = get_channel_videos(channel_id, limit=500)
# published_timestamps = [parse_publish_timestamp(video) for video in videos]
# publish_times = [time.hour + time.minute/60 for time in published_timestamps]
# plot_graph(publish_times)
# print(published_timestamps)
