# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale cinemasubito
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import httptools
from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "cinemasubito"
host = "https://www.cinemasubito.tv"
headers = [['Referer', host]]

def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand-pureita.cinemasubito mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange]  - Aggiornamenti[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange]  - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange]  - Anno[/COLOR]",
                     action="categorias_years",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange]  - Lista[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serie" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange]  - Aggiornate[/COLOR]",
                     action="peliculas_tv_new",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange]  - Nuovi Episodi[/COLOR]",
                     action="peliculas_tv_update",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def categorias(item):
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h4>Genere</h4>(.*?)</span>Ultime serie tv aggiornate</li>')

    # Estrae i contenuti 
    patron = '<a href="([^"]+)" title=".*?">\s*<li><span class="glyphicon glyphicon-zoom-in"></span>([^<]+)</li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
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
    bloque = scrapertools.get_match(data, 'Ultimi film usciti">(.*?)<h4>Genere</h4>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)"\s*title="[^>]+">\s*<li><span class="glyphicon glyphicon-menu-right"></span>([^<]+)</li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)
    

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace("streaming", "")
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
    logger.info("streamondemand-pureita cinemasubito " + item.url + " search " + texto)
    item.url = host + "/cerca/" + texto
    try:
        if item.extra == "movie":
            return peliculas(item)
        if item.extra == "serie":
            return peliculas_tv(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================		

def peliculas(item):
    logger.info("streamondemand-pureita cinemasubito peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">\s*<div class=".*?">\s*<img[^>]+src="([^"]+)"[^>]+alt="([^<]+)" title[^>]+>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '</span></li> <li><a href="([^"]+)" data-ci-pagination-page=".*?">'
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
	
def peliculas_tv(item):
    logger.info("streamondemand-pureita cinemasubito peliculas_tv")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">\s*<div class="tut">\s*' \
	         '<img src="([^"]+)" class="er" alt=".*?" title="([^<]+)">\s*</div>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    url_pagina = scrapertools.find_single_match(data, '</span></li> <li><a href="([^"]+)" data-ci-pagination-page=".*?">')
    if url_pagina != "":
        pagina = "[COLOR orange]"+"Pagina: "+ scrapertools.find_single_match(url_pagina, "pagina/([0-9]+)") + "[/COLOR]"
        itemlist.append(
            Item(channel = item.channel, 
                 action = "peliculas_tv", 
                 title = pagina,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",				 
                 url = url_pagina))
    return itemlist

# ==============================================================================================================================================================================

def peliculas_tv_update(item):
    logger.info("streamondemand-pureita cinemasubito peliculas_tv_update")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<li class="table1">(.*?)<h2 class="movies">Film Streaming</h2>')
	
    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">\s<li>\s*<p class="tohide">([^"]+)\s*-([^<]+)</p>'
    matches = re.compile(patron, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedepisode = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = scrapertools.unescape(match.group(1))

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[COLOR orange] -" + scrapedepisode + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_tv_new(item):
    logger.info("streamondemand-pureita cinemasubito peliculas_tv")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '</span>Ultime serie tv aggiornate</li>(.*?)</ul>')
	
    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">\s<li class=".*?"><img class="mini-thumb" src="([^"]+)" title="[^>]+" alt="([^<]+)"><span>'
    matches = re.compile(patron, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        scrapedthumbnail = scrapedthumbnail.replace("_mini", "")

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    return itemlist

# ==============================================================================================================================================================================
	
def episodios(item):
    logger.info("streamondemand.channels cinemasubito episodios")

    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<div style="display:none" id="accord">(.*?)</div>\s*</div>')

    patron = '<a style="font[^>]+" href="([^"]+)"><span class="glyphicon[^>]+"></span>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=host+scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True), tipo='tv'))

    return itemlist
	
# ==============================================================================================================================================================================
	
def findvideos(item):
    logger.info("streamondemand-pureita cinemasubito findvideos")

    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist



