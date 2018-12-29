# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale NetLover (search engine)"
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import re
import urllib
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "netlover"
DEBUG = config.get_setting("debug")
host = "https://www.netflixlovers.it"

TIMEOUT_TOTAL = 45

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand-pureita.netlover mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Top Del Mese - [COLOR red].NET Lover[/COLOR]",
                     action="film",
                     url="%s/classifiche/questo-mese" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_movie_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]TOP 7 Days - [COLOR red].NET Lover[/COLOR]",
                     action="film",
                     url="%s/classifiche/ultimi-7-giorni" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]The Best - [COLOR red].NET Lover[/COLOR]",
                     action="film",
                     url="%s/classifiche/netflix-originals" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_movie_P.png"),					 
               Item(channel=__channel__,
                     title="[COLOR azure]Serie TV - [COLOR red].NET Lover[/COLOR]",
                     url="%s/classifiche/serie-tv" % host,
                     action="film",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR red].NET Lover[/COLOR]",
                     action="film",
                     url="%s/classifiche/film" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Documentari - [COLOR red].NET Lover[/COLOR]",
                     action="film",
                     url="%s/classifiche/documentari" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_doc_P.png")]

    return itemlist

# ==============================================================================================================================================================================	

def serietv(item):
    logger.info("streamondemand-pureita.netlover serietv")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)"[^>]+>\s*[^>]+>\s*<span class="thumb-info-title">\s*<span class="thumb-info-caption-text">([^<]+)</span>.*?'
    patron += '<p>([^"]+)</p>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        scrapedtitle = scrapedtitle.replace(":", " -")
        scrapedtitle = scrapedtitle.replace("&#39;", " ")
        scrapedurl = ""
        scrapedtv = ".NET Lover"
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.split("(")[0]

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="do_search",
                 extra=urllib.quote_plus(scrapedtitle),
                 title=scrapedtitle + "[COLOR red]   " + scrapedtv + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 plot=scrapedplot,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" class="btn btn-borders btn-primary mr-xs mb-sm center">Mostra.*?</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="serietv",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def originals(item):
    logger.info("streamondemand-pureita.netlover film")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = 'alt="([^"]+)">\s*[^>]+>\s*[^>]+>\s*[^>]+>[^<]+[^>]+>[^>]+>\s*[^>]+>\s*'
    patron += '[^>]+>\s*<p>(.*?)<\/p>\s*<\/div>\s*[^>]+>\s*[^>]+>\s*[^>]+><a href[^>]+>([^<]+)<\/a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedplot, info in matches:
        scrapedtitle = scrapedtitle.replace(":", " -")
        scrapedtitle = scrapedtitle.replace("&#39;", " ")
        scrapedtitle = scrapedtitle.replace("Locandina di", "")
        scrapedurl = ""
        scrapedthumbnail = ""
        scrapedtv = ".NET Lover"
        #scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        #scrapedtitle = scrapedtitle.split("-")[0]

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="do_search",
                 extra=urllib.quote_plus(scrapedtitle),
                 title=scrapedtitle + "[COLOR red]   " + scrapedtv + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 plot=scrapedplot,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie" if not "Tv" in info else "tv"))


    patronvideos = '<a href="([^"]+)" class="btn btn-primary">Mostra .*?</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="originals",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def film(item):
    logger.info("streamondemand-pureita.netlover film")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = 'alt="([^"]+)">\s*[^>]+>\s*[^>]+>\s*[^>]+>[^<]+[^>]+>(.*?)<\/span>\s*[^>]+>[^>]+>\s*[^>]+>\s*[^>]+>.*?'
    patron += '<p>(.*?)</p>\s*[^>]+>\s*[^>]+>\s*[^>]+>\s*[^>]+>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, position, scrapedplot, info in matches:
        scrapedtitle = scrapedtitle.replace(":", " - ").replace("&#x27;", " ")
        scrapedtitle = scrapedtitle.replace("&#39;", " ")
        scrapedtitle=scrapedtitle.strip()
        scrapedthumbnail = ""
        scrapedurl = ""
        scrapedtv = ".NET Lover"
        #scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        #scrapedtitle = scrapedtitle.split("(")[0]

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="do_search",
                 extra=urllib.quote_plus(scrapedtitle),
                 title=position + " - " + scrapedtitle + "[COLOR red]   " + scrapedtv + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 plot=scrapedplot,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie" if "film" in info else "tv"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" class="btn btn-borders btn-primary mr-xs mb-sm center">Mostra.*?</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="film",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def do_search(item):
    from channels import buscador
    return buscador.do_search(item)

