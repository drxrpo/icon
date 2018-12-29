# -*- coding: utf-8 -*-

'''
    Eggman

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    thanks to MuadDib, FilmNet, Sirius & the others iv missed
'''

import re,urlparse,random,urllib

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import dom_parser2
from resources.lib.modules import log_utils
from resources.lib.modules import cfscrape

import requests
def url_ok(url):
    r = requests.head(url)
    if r.status_code == 200 or r.status_code == 301:
        return True
    else: return False

def HostChcker():
    if url_ok("https://vidics.unblocked.lat"):
        useurl = 'https://vidics.unblocked.lat/'
    elif url_ok("https://www.vidics.to"):
        useurl = 'https://www.vidics.to/'



    else: useurl = 'http://localhost/'
    
    return useurl

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['vidics.to']
        self.base_link = HostChcker()
        self.search_link = urlparse.urljoin(self.base_link, 'searchSuggest/FilmsAndTV/%s')
                       
    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title).replace('-','%20')
            url = self._search(clean_title)
            return url
        except Exception:
            return
            
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle).replace('-','%20')
            url = self._search(clean_title)
            return url
        except Exception:
            return
            
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            url += '-Season-%01d-Episode-%01d' % (int(season), int(episode))
            return url
        except Exception:
            return
            
    def _search(self, title):
        try:
            url = self.search_link % title
            headers =  {'Host': 'vidics.unblocked.mx',
                        'Origin': 'https://vidics.unblocked.mx',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'Referer': 'https://vidics.unblocked.mx/Film/%s' % title.replace('%20','_')}
            r = client.request(url, post='ajax=1', headers=headers)
            count = 0
            while len(r) == 0 and count <= 10:
                r = client.request(url, post='ajax=1', headers=headers)
                count += 1
            r = dom_parser2.parse_dom(r, 'tr')
            r = [urlparse.urljoin(self.base_link, re.findall("href='([^']+)", i.attrs['onclick'])[0]) for i in r]
            return r[0]
        except Exception:
            return
            
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if not url: return sources

            r = client.request(url)
            r = dom_parser2.parse_dom(r, 'div', {'class': 'movie_link'})
            r = [dom_parser2.parse_dom(i.content, 'a', req='href') for i in r]
            r = [(urlparse.urljoin(self.base_link, i[0].attrs['href']), i[0].content) for i in r]

            for i in r:
                try:
                    host = i[1].split('.')[0]
                    if host.lower() in str(hostDict):
                        sources.append({
                            'source': host,
                            'info': '',
                            'quality': 'SD',
                            'language': 'en',
                            'url': i[0],
                            'direct': False,
                            'debridonly': False
                        })
                    elif host.lower() in str(hostprDict):
                        sources.append({
                            'source': host,
                            'info': '',
                            'quality': 'SD',
                            'language': 'en',
                            'url': i[0],
                            'direct': False,
                            'debridonly': True
                        })
                except: 
                    pass
                    
            return sources
        except:
            return sources
            
    def resolve(self, url):
        try:
            r = client.request(url)
            r = dom_parser2.parse_dom(r, 'div', {'class': re.compile('movie_link\d')})
            r = [dom_parser2.parse_dom(i.content, 'a', req='href') for i in r]
            r = [i[0].attrs['href'] for i in r]
            url = r[0]
            return url
        except:
            return
