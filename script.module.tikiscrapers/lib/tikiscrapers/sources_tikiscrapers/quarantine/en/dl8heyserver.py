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
        self.domains = ['dl8.heyserver.in', 'dl9.heyserver.in']
        self.base_link_movie = 'http://dl9.heyserver.in/film/'
        self.base_link_tv = 'http://dl8.heyserver.in/serial/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            url = self.base_link_movie
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            title = '%s' % title
            url = self.base_link_tv % title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.se = 'S%02dE%02d' % (int(season), int(episode))
            season = 'S%02d/' % int(season)
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
            if 'serial' in result:
                try:
                    r = requests.get(result, timeout=5).content
                    r = re.findall('a href=".+?">(.+?)<', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '1080p.x265/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?">(.+?)<', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '1080p/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?">(.+?)<', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '720p.x265/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?">(.+?)<', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '720p/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?">(.+?)<', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '480p.x265/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?">(.+?)<', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url

                    result2 = result + '480p/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?">(.+?)<', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    return
            else:
                try:
                    result2 = result + '2018-10/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-11/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-12/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-3/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-4/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-5/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-6/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-7/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-8/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2018-9/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2019-1/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2019-2/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '2019-3/'
                    r = requests.get(result2, timeout=5).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['Dubbed']): raise Exception()
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    return
                    
            return sources
        except:
            return sources

    def resolve(self, url):
        return url

