import json
import urllib

import pickle
import requests

base_url = 'https://www.googleapis.com/youtube/v3/playlistItems?'

params = {'part': 'snippet',
          'maxResults': 50,
          'playlistId': 'UUzQUP1qoWDoEbmsQxvdjxgQ',
          'key': '{YOUTUBE_API_KEY'}

url = base_url + urllib.urlencode(params)
next_page_token = ''

video_ids = set()

while next_page_token is not None:

    j_response = json.loads(requests.get(url).text)
    items = j_response['items']

    for item in items:
        video_id = item['snippet']['resourceId']['videoId']
        video_ids.add(video_id)

    next_page_token = j_response.get('nextPageToken', None)
    params['pageToken'] = next_page_token
    url = base_url + urllib.urlencode(params)

with open('video_ids', 'w') as outfile:
    pickle.dump(list(video_ids), outfile)



