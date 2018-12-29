# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale altadefinizione01_wiki
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import os
import re
import time
import urllib
import urlparse

from core import httptools
from core import config 
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "altadefinizione01_wiki"
host = "https://www.altadefinizione4k.co/"
headers = [['Referer', host]]

def mainlist(item):
    logger.info("streamondemand-pureita altadefinizione01_wiki mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Al Cinema[/COLOR]",
                     action="peliculas_new",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Raccomandati[/COLOR]",
                     action="peliculas_top",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Aggiornati[/COLOR]",
                     action="peliculas_topnew",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url=host + "page/2/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Film[COLOR orange] - Anno[/COLOR]",
                     #action="categorias_years",
                     #url=host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Film[COLOR orange] - Paese[/COLOR]",
                     #action="categorias_country",
                     #url=host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================
	
def categorias(item):
    logger.info("streamondemand-pureita altadefinizione01_wiki categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '</i>Film per genere</div>(.*?)</ul>')

    # Extrae las entradas
    patron = '<li><a href="([^"]+)"><i class="fa fa-caret-right"></i>\s*([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:

         
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=host+scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita altadefinizione01_wiki ] " + item.url + " search " + texto)
    item.url = "%s/index.php?story=%s&do=search&subaction=search" % (host, texto)
    try:
        return peliculas_search(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
		
# ==============================================================================================================================================================================
	
def peliculas(item):
    logger.info("streamondemand-pureita altadefinizione01_wiki peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="short-img">\s*<a href="([^"]+)">'
    patron += '<img src="([^"]+)"  alt="([^<]+)" /></a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo="movie"))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<span class="pnext"><a href="([^"]+)">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist
	
# ==============================================================================================================================================================================
	
def peliculas_top(item):
    logger.info("streamondemand-pureita altadefinizione01_wiki peliculas_top")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a class="carou img-box" href="([^"]+)">\s*'
    patron += '<img data-src="([^"]+)" alt[^>]+>\s*<div class="rel-title">([^<]+)</div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo="movie"))

    return itemlist
	
# ==============================================================================================================================================================================
	
def peliculas_new(item):
    logger.info("streamondemand-pureita altadefinizione01_wiki peliculas_new")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="slide img-box">\s*<img data-src="([^"]+)" alt[^>]+>\s*<div class="rel-title">([^<]+)</div>\s*'
    patron += '<a class="carou-inner" href="([^"]+)"><i class[^>]+></i></a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo="movie"))

    return itemlist
	
# ==============================================================================================================================================================================

def peliculas_topnew(item):
    logger.info("streamondemand-pureita altadefinizione01_wiki peliculas_new")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, 'I migliori film.*?</div>(.*?)</div>\s*</div>')

    patron = '<div class="slide img-box">\s*<img data-src="([^"]+)" alt[^>]+>\s*'
    patron += '<div class="rel-title">([^<]+)</div>\s*'
    patron += '<a class="carou-inner" href="([^"]+)"><i class[^>]+></i></a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo="movie"))

    return itemlist
	
# ==============================================================================================================================================================================
	
def peliculas_search(item):
    logger.info("streamondemand-pureita altadefinizione01_wiki peliculas_new")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a class="sres-wrap clearfix" href="([^"]+)">\s*'
    patron += '<div class="sres-img"><img src="([^"]+)" alt="([^<]+)" />'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo="movie"))

    return itemlist
