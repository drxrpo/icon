# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canal SerieTvSubita
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# AndY
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "serietvsubita"
host = "http://serietvsubita.net"




def mainlist(item):
    logger.info("streamondemand-pureita serietvsubita mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Ultimi Episodi[/COLOR]",
                     action="peliculas_tv",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Lista[/COLOR]",
                     action="list_series",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Archivio A-Z[/COLOR]",
                     action="list_az",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Serie TV[COLOR orange][I] - Calendario Info [/I][/COLOR]",
                     #action="list_calendar",
                     #url='https://episodecalendar.com/en/calendar/public',
                     #extra="serie",
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]
    return itemlist

# ==============================================================================================================================================

def search(item, texto):
    logger.info("streamondemand-pureita serietvsubita search")
    itemlist = []
    item.extra = "search_tv"
	
    item.url = host + "/?s=" + texto + "&op.x=0&op.y=0"

    try:
        return peliculas_tv(item)
		
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================

def peliculas_tv(item):
    logger.info("streamondemand-pureita serietvsubita peliculas_tv")
    itemlist = []

    data = httptools.downloadpage(item.url).data	
    patron = '<div class="post-meta">\s*<a href="([^"]+)"\s*title="([^"]+)"\s*class=".*?"></a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        if "FACEBOOK" in scrapedtitle or "RAPIDGATOR" in scrapedtitle:
         continue
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))
				 
    # Extrae la marca de la siguiente página
    patron = '<strong class=\'on\'>\d+</strong>\s*<a href="([^<]+)">\d+</a>'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        if item.extra == "search_tv":
          next_page = next_page.replace('&#038;', '&')
        itemlist.append(
            Item(channel=__channel__,
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 action="episodes",
                 extra=item.extra,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================

def list_az(item):
    logger.info("streamondemand-pureita serietvsubita series")
    itemlist = []
    PERPAGE = 420

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas
    patron = '<li class="cat-item cat-item-\d+"><a href="([^"]+)" >([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedurl, scrapedtitle ) in enumerate(matches):
        scrapedplot = ""
        scrapedthumbnail = ""
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodes",
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png",
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True))
				 
    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="list_az",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist	
	
# ==============================================================================================================================================
	
def list_series(item):
    logger.info("streamondemand-pureita serietvsubita series")
    itemlist = []

    PERPAGE = 14

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas
    patron = '<li class="cat-item cat-item-\d+"><a href="([^"]+)" >([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedurl, scrapedtitle ) in enumerate(matches):
        scrapedplot = ""
        scrapedthumbnail = ""
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodes",
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo="tv"))
				 
    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="list_series",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================	
	
def episodes(item):
    logger.info("streamondemand-pureita serietvsubita episodes")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = '<div class="post-meta">\s*<a href="([^"]+)"\s*title="([^"]+)"\s*class=".*?"></a>.*?'
    patron += '<p><a href="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo="tv"))

    # Extrae el paginador
    patron = '<strong class=\'on\'>\d+</strong>\s*<a href="([^<]+)">\d+</a>'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 action="episodes",
                 extra=item.extra,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================

