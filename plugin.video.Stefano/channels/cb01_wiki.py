# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale cb01_wiki
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

__channel__ = "cb01_wiki"
host = "https://www.cb01.wiki"

headers = [['Referer', host]]

def mainlist(item):
    logger.info("streamondemand-pureita cb01_wiki mainlist")
	
	
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Raccomandati[/COLOR]",
                     action="peliculas_top",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Ultimi Aggiornati[/COLOR]",
                     action="peliculas",
                     url="%s/page/3/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/animazione/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

	
# ==============================================================================================================================================================================
	
def categorias(item):
    logger.info("streamondemand-pureita cb01_wiki categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '<span class="fa fa-film"></span>Film</a>(.*?)</ul>')

    # Extrae las entradas
    patron = '<li>\s*<a href="([^"]+)">\s*([^<]+)</a>\s*</li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if "Anime" in scrapedtitle:
          continue
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

def search(item, texto):
    logger.info("[streamondemand-pureita cb01_wiki ] " + item.url + " search " + texto)
    item.url = host + "/?do=search&mode=advanced&subaction=search&story=" + texto
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
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = '<div class="movie-cols clearfix">\s*<div class="[^>]+" data-link="([^"]+)">\s*'
    patron += '<img src="([^"]+)"\s*alt="([^<]+)"\s*\/>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        scrapedtitle = scrapedtitle.replace(" Streaming", "")

		
        html = httptools.downloadpage(scrapedurl).data

        patron = '<div class="video-player-plugin">([^+]+)<div class="wrapper-plugin-video">'
        matches = re.compile(patron, re.DOTALL).findall(html)
        for url in matches:
            if not "scrolling" in url:
                continue
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="movie",
                     title=scrapedtitle,
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     extra="movie",
                     thumbnail=scrapedthumbnail,
                     show=scrapedtitle,
                     folder=True), tipo="movie"))

    # Paginación
    patronvideos = r'<span>\d+</span> <a href="([^"]+)">\d+</a>'
    next_page = scrapertools.find_single_match(data, patronvideos)

    if next_page:
        scrapedurl = urlparse.urljoin(item.url, next_page)
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 extra=item.extra,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist	
	
# ==============================================================================================================================================================================
	
def peliculas_top(item):
    logger.info("streamondemand-pureita cb01_wiki peliculas_top")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="skoro-img img-box pseudo-link" data-link="([^"]+)">\s*'
    patron += '<img src="([^"]+)" alt="(.*?)"\s*\/>'

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
	
def peliculas_top2(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = '<div class="skoro-img img-box pseudo-link" data-link="([^"]+)">\s*'
    patron += '<img src="([^"]+)" alt="(.*?)"\s*\/>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        scrapedtitle = scrapedtitle.replace(":", " - ")
        scrapedtitle = scrapedtitle.replace(" Streaming", "")

        date = scrapertools.find_single_match(scrapedtitle, r'\((\d+)\)')
        scrapedtitle = scrapedtitle.replace(date, "")
        scrapedtitle = scrapedtitle.replace("(", "")
        scrapedtitle = scrapedtitle.replace(")", "")

		
        html = httptools.downloadpage(scrapedurl).data

        patron = '<div class="video-player-plugin">([^+]+)<div class="wrapper-plugin-video">'
        matches = re.compile(patron, re.DOTALL).findall(html)
        for url in matches:
            if not "scrolling" in url:
                scrapedtitle = scrapedtitle + " [[COLOR yellow]" + "Trailer" + "[/COLOR]] "
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="movie",
                     title=scrapedtitle + " [[COLOR yellow]" + date + "[/COLOR]]",
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     extra="movie",
                     thumbnail=scrapedthumbnail,
                     show=scrapedtitle,
                     folder=True), tipo="movie"))

    return itemlist	
