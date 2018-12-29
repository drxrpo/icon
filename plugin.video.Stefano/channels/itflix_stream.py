# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale itflix_stream
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import base64
import re
import urlparse

from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "itflix_stream"
host = "https://www.itflix.stream"
headers = [['Referer', host]]

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand-pureita [itflix_stream mainlist]")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas_list",
                     url="%s/film/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_new.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="genere",
                     url="%s/film/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Anno[/COLOR]",
                     action="year",
                     url="%s/film/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Popolari[/COLOR]",
                     action="peliculas",
                     url="%s/piu-popolari/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Raccomandati[/COLOR]",
                     action="peliculas",
                     url="%s/i-piu-votati/" %host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Sub ITA[/COLOR]",
                     action="peliculas",
                     url="%s/genere/sub-ita/" %host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_sub_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita itflix_stream] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return peliculas_search(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================

def peliculas_search(item):
    logger.info("streamondemand-pureita [itflix_stream peliculas_search]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)"\s*alt="(.*?)"\s*\/>.*?'
    patron += '<p>(.*?)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot  in matches:
        scrapedtitle =scrapedtitle.replace("[", "")
        scrapedtitle =scrapedtitle.replace("]", "") 
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie'))

    return itemlist		

# ==============================================================================================================================================================================		

def genere(item):
    logger.info("streamondemand-pureita [itflix_stream genere]")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = 'li class="cat-item cat-item-\d+"><a href="([^"]+)"\s*[^>]+>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def year(item):
    logger.info("streamondemand-pureita [itflix_stream genere]")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h2>Anno di rilascio</h2>(.*?)</ul>')
	
    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def peliculas(item):
    logger.info("streamondemand-pureita [itflix_stream peliculas]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<img src="([^"]+)"\s*alt="([^>]+)"><div class="rating">[^>]+></span>([^<]+)</div>'
    patron += '<div class="mepo">\s*<span class="quality">([^<]+)</span></div>\s*<a href="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, rating, quality, scrapedurl in matches:
        scrapedplot=""
        scrapedtitle = scrapedtitle.replace("[", "")
        scrapedtitle = scrapedtitle.replace("]", "")
        rating = rating.replace(" ", "")
        rating = rating.replace(",", ".")
        quality = quality.replace("PROSSIMAMENTE", "NA")
        if quality:
         quality = " [[COLOR yellow]" + quality + "[/COLOR]]"
        if rating:
         rating = " [[COLOR yellow]" + rating + "[/COLOR]]"
        if "Sub ITA"in quality:
          quality=quality.replace("Sub ITA", "[COLOR azure]] [[/COLOR]Sub ITA")	
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" +quality + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))

    # Extrae el paginador
    paginador = scrapertools.find_single_match(data, '<a class=\'arrow_pag\' href="([^"]+)">')
    if paginador != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=paginador,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_list(item):
    logger.info("streamondemand-pureita [itflix_stream peliculas_list]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<img src="([^"]+)"\s*alt="([^>]+)"><div class="rating">[^>]+></span>\s*[^"]+</div>'
    patron += '<div class="mepo">\s*<span class="quality">(.*?)</span></div>\s*<a href="([^"]+)">.*?'
    patron += '<span class[^>]+>\s*</span></div>[^>]+>[^>]+>([^<]+)</span>.*?'
    patron += '<div class="texto">([^<]+)</div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, quality, scrapedurl, rating, scrapedplot in matches:
        scrapedtitle = scrapedtitle.replace("[", "")
        scrapedtitle = scrapedtitle.replace("]", "")
        rating = rating.replace(",", ".")
        quality = quality.replace("PROSSIMAMENTE", "NA")
        if quality:
         quality = " [[COLOR yellow]" + quality + "[/COLOR]]"
        if rating:
         rating = " [[COLOR yellow]" + rating + "[/COLOR]]"
        if "Sub ITA"in quality:
         quality=quality.replace("Sub ITA", "[COLOR azure]] [[/COLOR]Sub ITA")		
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" +quality + rating,
                 thumbnail=scrapedthumbnail,
                 url=scrapedurl,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie'))

    # Extrae el paginador
    paginador = scrapertools.find_single_match(data, '<a class=\'arrow_pag\' href="([^"]+)"><i id=\'nextpagination\' class=\'icon-caret-right\'>')
    if paginador != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=paginador,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================

		
def findvideos(item):
    logger.info("streamondemand-pureita [itflix_stream  findvideos]")
    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.fulltitle, '[COLOR orange]' + videoitem.title + '[/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist



