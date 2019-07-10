# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 02-24-2019 by JewBMX in Scrubs.

import re,urllib,urlparse,base64
from tikiscrapers.modules import cleantitle,client,proxy,source_utils,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['sharemovies.net']
        self.base_link = 'http://sharemovies.net'
        self.search_link = '/search-movies/%s.html'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            q = cleantitle.geturl(title)
            q2 = q.replace('-','+')
            url = self.base_link + self.search_link % q2
            r = self.scraper.get(url).content
            match = re.compile('<div class="title"><a href="(.+?)">'+title+'</a></div>').findall(r)
            for url in match:
                return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return
 
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            q = url + '-season-' + season
            q2 = url.replace('-','+')
            url = self.base_link + self.search_link % q2
            r = self.scraper.get(url).content
            match = re.compile('<div class="title"><a href="(.+?)-'+q+'\.html"').findall(r)
            for url in match:
                url = '%s-%s.html' % (url,q)
                r = self.scraper.get(url).content
                match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
                for url in match:
                    return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            try:
                match = re.compile('themes/movies/img/icon/server/(.+?)\.png" width="16" height="16" /> <a href="(.+?)">Version ').findall(r)
                for host, url in match:
                    if host == 'internet':
                        pass
                    else:
                        valid, host = source_utils.is_host_valid(host, hostDict)
                        if valid:
                            sources.append({ 'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                sources = sources[:20]
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        r = self.scraper.get(url).content
        match = re.compile('Base64\.decode\("(.+?)"').findall(r)
        for iframe in match:
            iframe = base64.b64decode(iframe)
            match = re.compile('src="(.+?)"').findall(iframe)
            for url in match:
                return url

