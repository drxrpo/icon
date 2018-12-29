"""

    Copyright (C) 2018, TonyH


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

    -------------------------------------------------------------

    Usage Examples:

<dir>
<title> Moviefone Trailers</title>
<moviefone>trailers/1</moviefone>
</dir>

"""    

import requests,re,json,os
import koding
import __builtin__
import xbmc,xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode
from time import gmtime, strftime

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class MovieFone(Plugin):
    name = "moviefone"

    def process_item(self, item_xml):
        if "<moviefone>" in item_xml:
            item = JenItem(item_xml)
            if "trailers" in item.get("moviefone", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_moviefone_trailers",
                    'url': item.get("moviefone", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item


@route(mode='get_moviefone_trailers', args=["url"])
def get_game(url):
    xml = ""
    current = url.split("/")[-1]
    try:    
        url = "https://www.moviefone.com/movie-trailers/videos/?page="+current
        html = requests.get(url).content
        match = re.compile('"name": "(.+?)".+?"description": "(.+?)".+?thumbnailUrl": "(.+?)".+?"contentUrl": "(.+?)"',re.DOTALL).findall(html)
        for name,summary,thumbnail,link in match:
            name = name.replace("&#039;","")
            name = remove_non_ascii(name)
            summary = clean_search(summary)
            xml +=  "<item>"\
                    "<title>[B][I]%s[/B][/I]</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<summary>%s</summary>"\
                    "<link>%s</link>"\
                    "</item>" % (name,thumbnail,thumbnail,summary,link)            
        try:
            next_page = int(current)+1
            xml += "<dir>"\
                   "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
                   "<moviefone>trailers/%s</moviefone>"\
                   "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
                   "</dir>" % (next_page)                                  
        except:
            pass
    except:
        pass        
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 
              

def remove_non_ascii(text):
    return unidecode(text)

def clean_search(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', ' ', title)
    title = ' '.join(title.split())
    return title            
            