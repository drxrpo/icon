# -*- coding: utf-8 -*-

import xbmcaddon
import requests
from tikimeta.utils import fanarttv_client_key
# from tikimeta.utils import logger

# Code belongs to nixgates. Thankyou.

base_url = "http://webservice.fanart.tv/v3/%s/%s"
api_key = "a7ad21743fd710fccb738232f2fbdcfc"

def get_query(art):
    if art is None: return ''
    try:
        result = [(x['url'], x['likes']) for x in art if x.get('lang') == 'en']
        if not result: result = [(x['url'], x['likes']) for x in art]
        result = [(x[0], x[1]) for x in result]
        result = sorted(result, key=lambda x: int(x[1]), reverse=True)
        result = [x[0] for x in result][0]
        result = result.encode('utf-8')
    except:
        result = ''
    if not 'http' in result: result = ''
    return result

def get(query, remote_id):
    client_key = fanarttv_client_key()
    art = base_url % (query, remote_id)
    headers = {'client-key': client_key, 'api-key': api_key}
    art = requests.get(art, headers=headers).json()
    if query == 'movies':
        fanart_data = {'poster': get_query(art.get('movieposter')),
                        'fanart': get_query(art.get('moviebackground')),
                        'banner': get_query(art.get('moviebanner')),
                        'clearart': '',
                        'clearlogo': get_query(art.get('movielogo', []) + art.get('hdmovielogo', [])),
                        'landscape': get_query(art.get('moviethumb')),
                        'fanart_added': True}
    else:
        fanart_data = {'poster': get_query(art.get('tvposter')),
                        'fanart': get_query(art.get('showbackground')),
                        'banner': get_query(art.get('tvbanner')),
                        'clearart': get_query(art.get('clearart', []) + art.get('hdclearart', [])),
                        'clearlogo': get_query(art.get('hdtvlogo', []) + art.get('clearlogo', [])),
                        'landscape': get_query(art.get('tvthumb')),
                        'fanart_added': True}
    return fanart_data

def add(query, remote_id, meta):
    fanart_data = get(query, remote_id)
    meta['banner'] = fanart_data['banner']
    meta['clearart'] = fanart_data['clearart']
    meta['clearlogo'] = fanart_data['clearlogo']
    meta['landscape'] = fanart_data['landscape']
    meta['fanart_added'] = fanart_data['fanart_added']
    return meta

