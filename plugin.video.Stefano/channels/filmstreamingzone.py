# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale filmstreamingzone
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmstreamingzone"


DEBUG = config.get_setting("debug")

host = "https://www.filmstreaming.click/"

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
           ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
           ['Accept-Language', 'en-US,en;q=0.5'],
           ['Accept-Encoding', 'gzip, deflate']]

DEBUG = config.get_setting("debug")

def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand-pureita.filmstreamingzone mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Top[/COLOR]",
                     action="peliculas_top",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Novita'[/COLOR]",
                     action="peliculas",
                     url=host + "/novita-al-cinema/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Anno[/COLOR]",
                     action="categorias_years",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================	

def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '<ul class="hidden-menu clearfix">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li[^<]+<a href="([^"]+)">(.*?)<'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
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
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '</span>Film per Anno</a>(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================	

def search(item, texto):
    logger.info("[streamondemand-pureita.filmstreamingzone] " + item.url + " search " + texto)
    item.url = host + "/?do=search&subaction=search&story=" + texto
    try:
        if item.extra == "movie":
            return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================			
		
def peliculas_top(item):
    logger.info("streamondemand-pureita.filmstreamingzone peliculas_top")

    itemlist = []


    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, 'TOP DELLA SETTIMANA</div>(.*?)</ol>')

    # Extrae las entradas (carpetas)
    patron = '<a class="top-item" href="([^"]+)">.*?'
    patron += '<span>([^<]+)</span>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle, in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))


    return itemlist

# ==============================================================================================================================================================================	
	
def peliculas(item):
    logger.info("streamondemand-pureita.filmstreamingzone peliculas")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = r'<div class="movie-img[^=]+="([^"]+)">\s*<img src="([^"]+)" alt="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        year = scrapertools.find_single_match(scrapedtitle, r'\((\d{4})\)')
        scrapetrailar = " Trailer"

        
        html = httptools.downloadpage(scrapedurl).data

        patron = '<div class="video-player-plugin">([\s\S]*)<div class="wrapper-plugin-video">'
        matches = re.compile(patron, re.DOTALL).findall(html)
        for url in matches:
            if "scrolling" in url:
                scrapedtitle = scrapedtitle
            else:
                scrapedtitle = scrapedtitle + scrapetrailar

            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="movie",
                     title=scrapedtitle,
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     extra="movie",
                     thumbnail=scrapedthumbnail,
                     folder=True), tipo="movie"))

    patronvideos = r'<span class="pnext"><a href="(.*?)"><span class="fa fa-angle-double-right"></span>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 extra=item.extra,
                 folder=True))

    return itemlist	

