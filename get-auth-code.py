#!/usr/bin/python3

import urllib.parse

import secrets

query_params = urllib.parse.urlencode({
    'client_id': secrets.ACCESS_KEY,
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'response_type': 'code',
    'scope': 'public read_collections'
})

print(urllib.parse.urlunsplit((
    'https',
    'unsplash.com',
    'oauth/authorize',
    query_params,
    ''
)))

