'''
    BitLord
'''

import re, requests, xbmc
from tikiscrapers.modules import debrid, source_utils
from tikiscrapers.modules.control import logger

class source:

    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = 'http://www.bitlordsearch.com'
        self.search_link = 'http://www.bitlordsearch.com/get_list'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            return url
        except:
            print("Unexpected error in BitLord Script: episode", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return url

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle
            return url
        except:
            print("Unexpected error in BitLord Script: TV", sys.exc_info()[0])
            return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = url
            url = {'tvshowtitle': url, 'season': season, 'episode': episode, 'premiered': premiered}
            return url
        except:
            print("Unexpected error in BitLord Script: episode", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return url

    def sources(self, url, hostDict, hostprDict):
        sources = []
        if debrid.status() is False: raise Exception()
        if debrid.tor_enabled() is False: raise Exception()
        # try:
        logger('url', url)
        with requests.Session() as s:
            headers = {"Referer": self.domain,\
                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",\
                       "Host": "www.BitLord.com","User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0",\
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
                       "Accept-Encoding": "gzip, deflate, br","Accept-Language": "en-US,en;q=0.5",\
                       "Connection": "keep-alive","DNT":"1"}
            if 'episode' in url:
                iep = str(url['episode']).zfill(2)
                ise = str(url['season']).zfill(2)
                se = 's' + ise + 'e' + iep
                sel = url['tvshowtitle'].replace(' ','.') + '.' + se
                cate = '4'
            else:
                sel = url['title'].replace(' ','.') + '.' + str(url['year'])
                cate = '3'

            sel = sel.lower()
            bdata = {'filters[adult]': 'false', 'filters[category]': cate, 'filters[field]': 'category', 'filters[sort]': 'asc',\
                     'filters[time]': '4', 'limit': '25', 'offset': '0', 'query': sel}

            gs = s.post(self.search_link, data=bdata).text
            gl = re.compile('me\W+(.*?)[\'"].*?tih:(.*?)\W', re.I).findall(gs)
            logger('sel', sel)
            logger('gl', gl)
            for name, magnet in gl:
                quality, info = source_utils.get_release_quality(name, name)
                url = 'magnet:%s' % magnet
                sources.append({
                    'source': 'Torrent',
                    'quality': quality,
                    'language': 'en',
                    'url': url,
                    'direct': False,
                    'debridonly': True,
                    'info': info,
                })  
        return sources
        # except:
        #     print("Unexpected error in BitLord Script: Sources", sys.exc_info()[0])
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     print(exc_type, exc_tb.tb_lineno)
        #     return sources

        
    def resolve(self, url):
        return url