# -*- coding: utf-8 -*-
"""
**Created by Tempest**
"""

import re, requests

from tikiscrapers.modules import cleantitle
from tikiscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['s19.bitdl.ir']
        self.base_link_movie = 'http://s19.bitdl.ir/Movie/'
        self.base_link_tv = 'http://s19.bitdl.ir/Series/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            title = '%s.%s/' % (title, year)
            url = self.base_link_movie + title
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            url = self.base_link_tv + title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.se = 'S%02dE%02d' % (int(season), int(episode))
            season = '/S%02d/' % int(season)
            if not url: return
            url = url + season
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return

            result = url
            if 'Series' in result:
                r = requests.get(result, timeout=10).content
                r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                for url in r:
                    if not self.se in url: continue
                    url = result + url
                    quality = source_utils.check_direct_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            else:
                r = requests.get(result, timeout=10).content
                r = re.compile('a href="(.+?)" title=".+?"').findall(r)
                for url in r:
                    url = result + url
                    if any(x in url for x in ['Trailer', 'Dubbed', 'rar', 'EXTRAS']): continue
                    quality = source_utils.check_direct_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
