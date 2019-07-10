# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 02-24-2019 by JewBMX in Scrubs.
# Quality could be improved and tv shows needs coded in too.

import re
from tikiscrapers.modules import client,cleantitle,source_utils,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cinewhale.com']
        self.base_link = 'https://cinewhale.com'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + '/movies/%s-%s/' % (title,year)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                qual = re.compile('class="quality">(.+?)<').findall(r)
                for i in qual:
                    if 'HD' in i:
                        quality = 'HD'
                    else:
                        quality = 'SD'
                match = re.compile('<a href="(.+?)" target="_blank" class').findall(r)
                for url in match:
                    r = self.scraper.get(url).content
                    match = re.compile('iframe src=&quot;(.+?)/&quot;').findall(r)
                    for url in match:
                        info = i
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False}) 
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url


#https://cinewhale.com/search?q=deadpool+2+2018
#https://cinewhale.com/movies/aquaman-2018
#https://cinewhale.com/movies/robin-hood-2018
#https://cinewhale.com/tvshows/star-wars-resistance-2018
#<div class="episode-number">15</div>
#                <ul class="embeds-list clearfix">
#                                    <li>
#                    <a href="https://linkth.is/embed/EQylfdphYcc" target="_blank">Openload</a>
#                  </li>
#                                    <li>
#                    <a href="https://streamelon.com/embed/EQylfdphYcc" target="_blank">Streamango</a>
#                  </li>

