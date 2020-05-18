#!/usr/bin/python3

import json
import urllib.parse
import urllib.request
import sys

import secrets

auth_code = sys.argv[1]

url = urllib.parse.urlunsplit((
    'https',
    'unsplash.com',
    'oauth/token',
    '',
    ''
))

params = urllib.parse.urlencode({
    'client_id': secrets.ACCESS_KEY,
    'client_secret': secrets.SECRET_KEY,
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'code': auth_code,
    'grant_type': 'authorization_code'
})

request = urllib.request.Request(
    url,
    data=params.encode('utf-8'),
    method='POST'
)

response = urllib.request.urlopen(request)

print(response.status, response.reason)
if response.status == 200:
    data = json.loads(response.read())
    with open('config.json', 'w') as config_file:
        json.dump(data, config_file)


