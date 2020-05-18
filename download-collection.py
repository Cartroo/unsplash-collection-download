#!/usr/bin/python3

import argparse
import itertools
import json
import os
import re
import sys
import urllib.parse
import urllib.request

NON_WORD_REGEX = re.compile(r'[\W]+')

def get_next_link(headers):
    for link_spec in headers.get('Link', '').split(','):
        if ';' not in link_spec:
            continue
        url, rel = link_spec.split(';', 1)
        if '=' not in rel:
            continue
        rel_token, rel_type = rel.split('=', 1)
        if rel_token.strip().lower() != 'rel':
            continue
        if rel_type.strip().strip('"').lower() == 'next':
            return url.strip().lstrip('<').rstrip('>')
    return None

def make_authorised_request(config, url):
    auth_header = config['token_type'] + ' ' + config['access_token']
    request = urllib.request.Request(
        url,
        headers={'Authorization': auth_header}
    )
    return urllib.request.urlopen(request)

def make_paginated_request(config, url):
    # Empty list to build return value.
    ret = []
    # Iterate across response pages.
    while url is not None:
        # Make the request and add result to return list.
        response = make_authorised_request(config, url)
        ret += json.loads(response.read())
        # Check for next page link.
        url = get_next_link(response.headers)
    return ret

def get_file(config, url, dest_path):
    print('Downloading %r' % (dest_path,))
    response = make_authorised_request(config, url)
    with open(dest_path, 'wb') as fd:
        while True:
            data = response.read(8192)
            if not data:
                break
            fd.write(data)

def get_collections(config):
    url = 'https://api.unsplash.com/users/'+config['username']+'/collections'
    return make_paginated_request(config, url)

def list_collections(config):
    collections = get_collections(config)
    print('Collections for ' + config['username'] + ':')
    for collection in collections:
        print('  - [' + str(collection['id']) + '] ' + collection['title'])

def find_collection(config, collection_id):
    collections = get_collections(config)
    for collection in collections:
        if collection_id == collection['id']:
            return collection
    raise Exception('Collection ' + repr(collection_id) + ' not found')

def make_filename(input_str):
    return '-'.join(NON_WORD_REGEX.split(input_str)).lower().strip('-')[:250]

def get_already_downloaded(download_dir):
    already_downloaded = set()
    for entry in os.listdir(download_dir):
        basename, ext = os.path.splitext(entry)
        if ext.lower() not in ('.jpg', 'jpeg'):
            continue
        if '@' not in basename:
            continue
        already_downloaded.add(basename.split('@', 1)[1])
    return already_downloaded

def download_collection(config, collection_id):
    download_dir = config['download_dir']
    already_downloaded = get_already_downloaded(download_dir)
    collection = find_collection(config, collection_id)
    photos = make_paginated_request(config, collection['links']['photos'])
    for photo in photos:
        if photo['id'] not in already_downloaded:
            download_url = photo['urls']['full']
            filename = '@'.join((
                make_filename(photo['alt_description'])[:160],
                photo['id'])) + '.jpg'
            get_file(config, download_url, os.path.join(download_dir, filename))

parser = argparse.ArgumentParser(description='Download collection photos')
parser.add_argument('--list', action='store_true', default=False,
                    help='list collections')
parser.add_argument('--collection', type=int, default=None,
                    help='collection ID to download')
parser.add_argument('--config', default='./config.json',
                    help='config filename')

args = parser.parse_args()
with open(args.config) as config_file:
    config = json.load(config_file)
if args.list:
    list_collections(config)
elif args.collection is not None:
    download_collection(config, args.collection)


