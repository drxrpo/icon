# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA- XBMC Plugin
# Canale filmstreamingita
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import re

from core import logger
from core import httptools
from core import config
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmstreamingita"
host = "http://filmstreamingita.xyz"
headers = [['Referer', host]]



def mainlist(item):
    logger.info("streamondemand-pureita.filmstreamingita mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/category/animazione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorie",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("streamondemand-pureita.filmstreamingita search")
    item.url = host + "/?s=" + texto
    try:
        return peliculas(item)

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================

def categorie(item):
    logger.info("streamondemand-pureita.filmstreamingita categorie")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data 
    blocco = scrapertools.get_match(data, r'Genere Film</a>(.*?)</ul>')
    patron = r'<li id=".*?" class=".*?"><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def peliculas(item):
    logger.info("streamondemand-pureita.filmstreamingita peliculas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data 

    patron = r'<div class="home_tall_box">\s*'
    patron += r'<a href="([^"]+)".*?>\s*<img.*?alt="([^"]+)".*?src="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapedtitle.replace("’", "'")
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="movie",
                 plot=scrapedplot,
                 show=scrapedtitle,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie"))


    patron = '<li><a href="([^"]+)" class="next">&raquo;</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 extra=item.extra,
                 folder=True))

    patron = '<a class="next page-numbers" href="([^"]+)">Successivo &raquo;</a></center>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 extra=item.extra,
                 folder=True))
    return itemlist

# ==============================================================================================================================================================================

def findvideos(item):
    logger.info("streamondemand-pureita.filmstreamingita findvideos")
    data = httptools.downloadpage(item.url, headers=headers).data 
    
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(['[COLOR orange][B]' + server + ' [/COLOR][/B]-' + item.show])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__
    return itemlist

# ==============================================================================================================================================================================

    



