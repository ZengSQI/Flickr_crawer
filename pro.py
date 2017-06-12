import requests
import re

r = requests.get('https://www.flickr.com/photos/136296496@N07')

x = re.search('href="/account/upgrade/pro"', r.content.decode('utf-8'))

if x:
    print('a')
