# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # # -*- coding: UTF-8 -*-
'''
    A scraper for SelflessLive.

    Updated and refactored by someone.
    Originally created by others.
'''

 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Selfless Live
# Addon id: plugin.video.selfless
# Addon Provider: Kodi Ghost

import re,traceback,json,urllib,urlparse,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['afdah.org']
        self.base_link = 'http://afdah.org/'
        self.search_link = '%s/search?q=afdah.org+%s+%s'
        self.goog = 'https://www.google.co.uk'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('AFDAH - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None: return

            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            title = urldata['title']
            year = urldata['year']
            
            scrape = title.lower().replace(' ','+').replace(':', '')

            start_url = self.search_link %(self.goog,scrape,year)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

            html = client.request(start_url,headers=headers)
            results = re.compile('href="(.+?)"',re.DOTALL).findall(html)

            for url in results:
                if self.base_link in url:
                    if 'webcache' in url:
                        continue
                    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
                    html = client.request(url,headers=headers)
                    
                    chktitle = re.compile('property="og:title" content="(.+?)" ',re.DOTALL).findall(html)[0]
                    if cleantitle.get(title) in cleantitle.get(chktitle):
                        # pulls all the links from Alternate Servers tab
                        alt_server_cont = re.compile('<div id="cont_5" class="tabContent" style=".+?">(.+?)</div>',re.DOTALL).findall(html)[0]
                        alt_links = re.compile('<a rel="nofollow" href="(.+?)"',re.DOTALL).findall(alt_server_cont)
                        for vid_url in alt_links:
                            host = vid_url.split('//')[1].replace('www.','')
                            host = host.split('/')[0].lower()
                            sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': vid_url, 'info': [], 'direct': False, 'debridonly': False})
                    return sources
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('AFDAH - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url