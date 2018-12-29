# -*- coding: utf-8 -*-
#------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# CanalE  hdblog
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
#------------------------------------------------------------

import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "hdblog"
host = "https://www.hdblog.it"
headers = [['Referer', host]]



def mainlist(item):
    logger.info("[streamondemand-pureita hdblog] mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Recensioni[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/video/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/rev_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Recensioni[COLOR orange] - Hardware[/COLOR]",
                     action="peliculas",
                     url="https://hardware.hdblog.it/video/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/pc_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Recensioni[COLOR orange] - Android[/COLOR]",
                     action="peliculas",
                     url="https://android.hdblog.it/video/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/android_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Recensioni[COLOR orange] - Windows[/COLOR]",
                     action="peliculas",
                     url="https://windows.hdblog.it/video/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/windows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Recensioni[COLOR orange] - IOS[/COLOR]",
                     action="peliculas",
                     url="https://apple.hdblog.it/video/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/ios_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Recensioni[COLOR orange] - AltaDefinizione[/COLOR]",
                     action="peliculas",
                     url="https://altadefinizione.hdblog.it/video/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/vid_camera_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Recensioni[COLOR orange] - Games[/COLOR]",
                     action="peliculas",
                     url="https://games.hdblog.it/video/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/games1_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Cerca ...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]



    return itemlist

# ==================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita hdblog] " + item.url + " search " + texto)

    item.url = "%s/?sName=recensione %s" % (host, texto)
    try:
        return peliculas_src(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []	

# ==================================================================================================================================================
		
def peliculas_src(item):
    logger.info("[streamondemand-pureita hdblog] peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = 'data-src="([^"]+)"[^>]+>\s*[^>]+></span>\s*'
    patron += '</a>\s*<div class="title_.*?">\s*'
    patron += '<a href="([^"]+)"[^>]+>\s*(.*?)\s*</a>' 
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if  "recensione-da-hdblog/" in scrapedurl or "recensione da HDblog" in scrapedtitle:
         continue
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True) )

    # Extrae el paginador
    patronvideos  = '<a style="[^"]+" href="([^"]+)" class="esteso">Prossima pagina</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def peliculas(item):
    logger.info("[streamondemand-pureita hdblog] peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img width=".*?" height=".*?" alt="" data-src="([^"]+)" src="[^>]+"/>\s*</a>\s*'
    patron += '<a href="([^"]+)"\s*'
    patron += 'class="title_link">\s*(.*?)\s*</' 
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True) )

    # Extrae el paginador
    patronvideos  = '<a style="[^"]+" href="([^"]+)" class="esteso">Prossima pagina</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
