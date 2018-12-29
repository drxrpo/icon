# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale per il sito cineblog01_show
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

__channel__ = "cineblog01_show"
host = "http://www.cineblog01.show"
headers = [['Referer', host]]


def mainlist(item):
    logger.info("streamondemand-pureita cineblog01.show mainlist")
		
    itemlist = [#Item(channel=__channel__,
                     #title="[COLOR azure]Film[COLOR orange] - Ultimi Aggiornati[/COLOR]",
                     #action="peliculas",
                     #url=host+"/page/6/",
                     #extra="movie",
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
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
                     title="[COLOR azure]Film[COLOR orange] - Per Anno[/COLOR]",
                     action="categorias_year",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Per Paese[/COLOR]",
                     action="categorias_country",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist
	
# =============================================================================================================================================================
	
def categorias(item):
    logger.info("streamondemand-pureita cineblog01.show categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '<div class=" genre_list">(.*?)Film Streaming</a></li>')

    # Extrae las entradas
    patron = '<li><a href="(.*?)">\s*([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if "Anime" in scrapedtitle:
          continue
        scrapedurl = host + scrapedurl
        if "avventura" in scrapedurl:
         scrapedurl = scrapedurl + "page/2/"			
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist
	
# =============================================================================================================================================================

def categorias_year(item):
    logger.info("streamondemand-pureita cineblog01.show categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, 'Film per anno</a>(.*?)</ul>')

    # Extrae las entradas
    patron = '<li><a href="([^<]+)">Film Streaming\s*(.*?)</a></li>'
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

	
# =============================================================================================================================================================

def categorias_country(item):
    logger.info("streamondemand-pureita cineblog01.show categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, 'Film per Paese</a>(.*?)</ul>')

    # Extrae las entradas
    patron = '<li><a\s*href="(.*?)">\s*(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl      
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png",
                 folder=True))

    return itemlist

# =============================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita cineblog01.show ] " + item.url + " search " + texto)
    item.url = host + "/?do=search&mode=advanced&subaction=search&story=" + texto
    try:
        return peliculas_search(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
		

# =============================================================================================================================================================

def peliculas(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = '<\/div>\s*<a href="([^"]+)">\s*<figure>'
    patron += '<img src="([^"]+)" alt="(.*?)">.*?'
    patron += '<div class="descr">(.*?)<\/div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:

        scrapedtitle = scrapedtitle.replace(" Streaming", "")
        scrapedthumbnail = host + scrapedthumbnail
        #date = scrapertools.find_single_match(scrapedtitle, r'\((\d+)\)')
        #scrapedtitle = scrapedtitle.replace(date, "")
        #scrapedtitle = scrapedtitle.replace("(", "")
        #scrapedtitle = scrapedtitle.replace(")", "")

		
        html = httptools.downloadpage(scrapedurl).data

        patron = '<div class="video-player-plugin">([^+]+)<div class="wrapper-plugin-video">'
        matches = re.compile(patron, re.DOTALL).findall(html)
        for url in matches:
            if not "scrolling" in url:
              continue
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="movie",
                     title=scrapedtitle,
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     extra="movie",
                     thumbnail=scrapedthumbnail,
                     show=scrapedtitle,
                     plot=scrapedplot,
                     folder=True))

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

	
# =============================================================================================================================================================

def peliculas_search(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = '<div class="title"><a href="([^"]+)">[^<]+</a>\s*<\/div>\s*'
    patron += '<div class="alt_name">(.*?)</div>.*?'
    patron += '<figure><img src="([^"]+)" alt[^>]+></figure>.*?'
    patron += '<div class="descr">(.*?)<\/div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedplot in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace(" Streaming", "")
        scrapedthumbnail = host + scrapedthumbnail
        #date = scrapertools.find_single_match(scrapedtitle, r'\((\d+)\)')
        #scrapedtitle = scrapedtitle.replace(date, "")
        #scrapedtitle = scrapedtitle.replace("(", "")
        #scrapedtitle = scrapedtitle.replace(")", "")

		
        html = httptools.downloadpage(scrapedurl).data

        patron = '<div class="video-player-plugin">([^+]+)<div class="wrapper-plugin-video">'
        matches = re.compile(patron, re.DOTALL).findall(html)
        for url in matches:
            if not "scrolling" in url:
              continue
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     title=scrapedtitle,
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     extra="movie",
                     thumbnail=scrapedthumbnail,
                     show=scrapedtitle,
                     plot=scrapedplot,
                     folder=True))

    return itemlist

