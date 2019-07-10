# -*- coding: UTF-8 -*-

import re,urllib,urlparse
from tikiscrapers.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['fmovies.io']
        self.base_link = 'https://www11.fmovies.io'
        self.search_link = '/search.html?keyword=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url)
            match = re.compile('<a href="/watch/(.+?)" title="(.+?)">',re.DOTALL).findall(search_results)
            for row_url, row_title in match:
                row_url = 'https://www11.fmovies.io/watch/%s' % row_url
                if cleantitle.get(title) in cleantitle.get(row_title):
                    return row_url
            return
        except:
            return

# https://www11.fmovies.io/watch/we-bare-bears-season-4-episode-47-lord-of-the-poppies.html
# https://www11.fmovies.io/watch/fbi-season-1-episode-18-most-wanted.html

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources
            html = client.request(url)
            quality = re.compile('<div>Quanlity: <span class="quanlity">(.+?)</span></div>',re.DOTALL).findall(html)
            for qual in quality:
                quality = source_utils.check_url(qual)
            links = re.compile('var link_.+? = "(.+?)"',re.DOTALL).findall(html)
            for url in links:
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url

