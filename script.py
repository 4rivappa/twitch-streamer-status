from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio
import json
import os

async def get_streamer_details():
    client_id = os.environ['TWITCH_CLIENT_ID']
    client_secret = os.environ['TWITCH_CLIENT_SECRET']
    twitch = await Twitch(client_id, client_secret)

    user = await first(twitch.get_users(logins='timeenjoyed'))

    ## getting videos

    videos_list = []
    async for video in twitch.get_videos(user_id = user.id):
        curr_video = dict()
        curr_video['url'] = video.url
        curr_video['title'] = video.title
        curr_video['created_at'] = video.created_at
        videos_list.append(curr_video)

    mini_videos_list = videos_list[:3]

    ## getting stream details

    streams_list = []
    async for stream in twitch.get_streams(user_id = user.id, first=10):
        curr_stream = dict()
        curr_stream['title'] = stream.title
        curr_stream['started_at'] = stream.started_at
        streams_list.append(curr_stream)
        break

    data = dict()
    data['videos'] = videos_list
    data['streams'] = streams_list

    if not os.path.exists('exports'):
        os.makedirs('exports')

    with open('./exports/data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True, default=str)
    
    data['videos'] = mini_videos_list
    with open('./exports/mini_data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True, default=str)

    await twitch.close()

asyncio.run(get_streamer_details())