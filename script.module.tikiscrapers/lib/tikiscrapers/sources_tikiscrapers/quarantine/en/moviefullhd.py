# -*- coding: utf-8 -*-

'''
    **Created by Tempest**
'''

import re, urllib,urlparse, requests

from tikiscrapers.modules import cleantitle
from tikiscrapers.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviefull-hd.org']
        self.base_link = 'https://moviefull-hd.org'
        self.search_movie = '/movie/%s-%s'
        self.search_tv = '/movie/%s-season-%s/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_movie % (title, year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = self.base_link + self.search_tv % (url['tvshowtitle'], season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = requests.get(url).content
            u = client.parseDOM(r, "div", attrs={"class": "netflix"})
            for t in u:
                u = re.compile('src="(.+?)"').findall(t)
                for url in u:
                    sources.append({'source': 'CDN', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
