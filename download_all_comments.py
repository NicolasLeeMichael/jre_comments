import json
import urllib

import pickle
import requests

from datetime import datetime

base_url = 'https://www.googleapis.com/youtube/v3/commentThreads?'

params = {'part': 'snippet',
          'maxResults': 100,
          'searchTerms': 'joe,rogan',
          'key': '{YOUTUBE_API_KEY'}

with open('video_ids', 'rU') as f:
    video_ids = pickle.load(f)

for video_id in video_ids:
    params['videoId'] = video_id

    params.pop('pageToken', None)
    url = base_url + urllib.urlencode(params)

    next_page_token = ''

    while next_page_token is not None:

        j_response = json.loads(requests.get(url).text)

        time_stamp = datetime.utcnow().strftime('%Y%m%d%H-%M%S.%f')[:-3]
        filename = 'jre_comments_' + params['videoId'] + '_' + time_stamp + '.json'

        with open(filename, 'w') as outfile:
            json.dump(j_response, outfile)

        next_page_token = j_response.get('nextPageToken', None)
        params['pageToken'] = next_page_token
        url = base_url + urllib.urlencode(params)



