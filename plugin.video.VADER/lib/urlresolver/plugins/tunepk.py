'''
tunepk urlresolver plugin
Copyright (C) 2013 icharania

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import re
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

import xbmc
import json
import xbmc
import requests

class TunePkResolver(UrlResolver):
    name = "tune.pk"
    domains = ["tune.pk"]
    pattern = '(?://|\.)(tune\.pk)/(?:player|video|play)/(?:[\w\.\?]+=)?(\d+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        vUrl = None
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        link = requests.get(web_url, verify=False, headers=headers).text
        xbmc.log(link)

        if link.find('404 Not Found') >= 0:
            raise ResolverError('The requested video was not found.')

        videoUrl = []

        jsonObj = json.loads(link)

        vUrl = jsonObj['data']['details']['player']['sources'][0]['file']

        # for source in sources:
        #     video_link = str(re.compile('"file":"(.*?)"').findall(source)[0])
        #     videoUrl.append(video_link)
        #
        # vUrl = ''
        # vUrlsCount = len(videoUrl)
        # if vUrlsCount > 0:
        #     q = self.get_setting('quality')
        #     if q == '0':
        #         # Highest Quality
        #         vUrl = videoUrl[0]
        #     elif q == '1':
        #         # Medium Quality
        #         vUrl = videoUrl[(int)(vUrlsCount / 2)]
        #     elif q == '2':
        #         # Lowest Quality
        #         vUrl = videoUrl[vUrlsCount - 1]


        if vUrl != None:
            return vUrl+'|User-Agent=Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_11_6%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F58.0.3029.110%20Safari%2F537.36'
        else:
            raise ResolverError('No playable video found.')

    def get_url(self, host, media_id):
        url = 'https://tune.pk/api_public/playerConfigs/?api_key=777750fea4d3bd585bf47dc1873619fc&id={media_id}&autoplay=yes&embed=true&country=ca'.format(media_id=media_id)
        return url

    @classmethod
    def get_settings_xml(cls):
        xml = super(cls, cls).get_settings_xml()
        xml.append('<setting label="Video Quality" id="%s_quality" type="enum" values="High|Medium|Low" default="0" />' % (cls.__name__))
        return xml
