#!/usr/bin/python3
import re
import json
import requests
import xmltodict
from collections import OrderedDict


class FeedFlip:
    def __init__(self):
        self.session = requests.session()

    def convert(self, url_or_id):
        base_lookup_query_string = {
            'id':     None,
            'entity': 'podcast'
        }
        base_lookup_link = 'https://itunes.apple.com/lookup'
        if type(url_or_id) is str:
            url_or_id = re.findall(r'\d+', url_or_id)[0]
        base_lookup_query_string['id'] = url_or_id
        response = self.session.request('GET', base_lookup_link, params=base_lookup_query_string)
        rss_url = response.json()['results'][0]['feedUrl']
        print(f'RSS URL: {rss_url}')
        self.parse_xml(rss_url)

    def parse_xml(self, rss_url):
        episode_dict = {}
        response = self.session.request('GET', rss_url)
        podcast_dict = dict(xmltodict.parse(response.content))
        episodes = podcast_dict['rss']['channel']['item']
        for e in episodes:
            try:
                # implement update() method
                episode_dict[e['title']] = {
                    'description':e['itunes:summary'],
                    'pubDate':e['pubDate'],
                    'url':e['enclosure']['@url'],
                    'length':e['itunes:duration']
                }
            except:
                continue
            self.download(e['enclosure']['@url'], e['title'])
        print(json.dumps(episode_dict, indent=4))

    def download(self, url, title=None):
        print(f'Downloading {title}...')
        file_extension = url.split('.')[-1]
        r = self.session.request('GET', url, stream=True)
        with open(f'{title}.{file_extension}', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        return local_filename

ff = FeedFlip()
#ff.convert('https://itunes.apple.com/us/podcast/kfc-radio/id536209167?mt=2')
ff.convert('https://itunes.apple.com/us/podcast/hard-factor/id1396058631?mt=2')
