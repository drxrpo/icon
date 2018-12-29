# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  altastreaming
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# -----------------------------------------------------------------

import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "altastreaming"
host = "http://altastreaming.pink/"
headers = [['Referer', host]]

def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand-pureita.altastreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Al Cinema[/COLOR]",
                     action="peliculas",
                     url="%s/al-cinema/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/film/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Sub ITA[/COLOR]",
                     action="peliculas",
                     url="%s/sub-ita/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_sub_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Per Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Per Qualita'[/COLOR]",
                     action="categorias_quality",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Per Anno[/COLOR]",
                     action="categorias_years",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================
	
def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<ul class="listSubCat" id="Film">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def categorias_years(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<ul class="listSubCat" id="Anno">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def categorias_quality(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<ul class="listSubCat" id="Qualita">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def search(item, texto):
    logger.info("streamondemand-pureita.altastreaming " + item.url + " search " + texto)
    item.url = host + "/?do=search&subaction=search&story=" + texto
    try:
     return peliculas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
		
# ==============================================================================================================================================================================		
		
def peliculas(item):
    logger.info("streamondemand-pureita.altastreaming peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a\s*href="[^>]+>([^<]+)<\/a><\/span>\s*<a\s*href="([^"]+)"><img src="([^"]+)"\s*class[^>]+alt="(.*?)"[^>]+><\/a>\s*<div class="info">.*?<\/strong>\s*(.*?)<\/div>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        votos = scrapertools.unescape(match.group(5))
        scrapedtitle = scrapertools.unescape(match.group(4))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(2))
        quality = scrapertools.unescape(match.group(1))
        if votos=="":
          votos="N/A"
        info = " [COLOR yellow] [" + quality + "] [" + votos + "][/COLOR]"

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="peliculas_server",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle + info,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">Succ →</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================	
		
def peliculas_server(item):
    logger.info("streamondemand-pureita.altastreaming peliculas_server")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, "<li>guardaRE <strong>FILM HD ITA</strong></li>(.*?)</ul>")
    # Extrae las entradas (carpetas)
    patron = '<li><a href=".*?" data-target="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if scrapedtitle.startswith("Nikmax"):
            continue
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=item.title,
                 show=scrapedtitle,
                 title="[COLOR azure]" + item.title + "[COLOR yellow] [" + scrapedtitle + "][/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True), tipo='movie'))

    return itemlist

# ==============================================================================================================================================================================
		
def findvideos(item):
    logger.info("streamondemand-pureita.altastreaming findvideos")
    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.fulltitle, '[COLOR orange][B]' + videoitem.title + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
