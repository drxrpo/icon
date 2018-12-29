# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  altadefinizione01
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger, httptools
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "altadefinizione01"


DEBUG = config.get_setting("debug")

host = "http://www.altadefinizione01.io/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand-pureita.altadefinizione01 mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas_new",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_new.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - In Vetrina[/COLOR]",
                     action="peliculas_home",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/streaming/animazione/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animation2_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, 'Film per genere</div>(.*?)</button>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)"> <img src=".*?" alt=""> <span>([^<]+)'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
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
    logger.info("pureita.altadefinizione01 " + item.url + " search " + texto)
    item.url = host + "/?do=search&subaction=search&story=" + texto
    try:
        if item.extra == "movie":
            return peliculas(item)
        if item.extra == "serie":
            return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================
		
def peliculas(item):
    logger.info("pureita.altadefinizione01 peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="short_content">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)" alt="[^"]+" class="shortstory-img" />\s*<div class="short_header">\s*([^<]+)</div>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a\s*href="([^"]+)">&#62;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def peliculas_new(item):
    logger.info("pureita.altadefinizione01 peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, 'Ultimi inseriti / Tutte le categorie</div>(.*?)</div>\s*<script>')

    # Extrae las entradas (carpetas)
    patron = '<div class="short_content">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)" alt="[^"]+" class="shortstory-img" />\s*<div class="short_header">\s*([^<]+)</div>'
    matches = re.compile(patron, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a\s*href="([^"]+)">&#62;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_new",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def peliculas_home(item):
    logger.info("pureita.altadefinizione01 peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, '<section class="container">(.*?)Film per genere</div>')

    # Extrae las entradas (carpetas)
    patron = '<div class="short_content">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)" alt="[^"]+" class="shortstory-img" />\s*<div class="short_header">\s*([^<]+)</div>'
    matches = re.compile(patron, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))
    return itemlist

# ==============================================================================================================================================================================
	
def findvideos(item):

    data = scrapertools.anti_cloudflare(item.url, headers)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR orange][B]' + videoitem.title + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist

# ==============================================================================================================================================================================
"""	

# ==============================================================================================================================================================================	
	
def categorias_years(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, '</ul>\s*<ul class="cf">(.*?)<ul class="cf">')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def categorias_country(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, '</a></li>\s*</ul>\s*<ul class="cf">(.*?)</ul>\s*</div>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">([^<]+)</a></li> '
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_years_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_tv(item):
    logger.info("pureita.altadefinizione01 peliculas_tv")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<section class="main">(.*?)</section>'
    data = scrapertools.find_single_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<h2 class="titleFilm"><a href="([^"]+)">(.*?)</a></h2>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="seasons",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<span>.*?</span>.*?href="(.*?)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist


def seasons(item):
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<li><a href="([^"]+)" data-toggle="tab">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedseason in matches:
        scrapedurl = item.url + scrapedurl
        scrapedtitle = item.title

        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + " " + "Stagione " + scrapedseason,
                 url=scrapedurl,
                 thumbnail=item.scrapedthumbnail,
                 plot=item.scrapedplot,
                 folder=True))

    return itemlist


def episodios(item):
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = 'class="tab-pane fade" id="%s">(.*?)class="tab-pane fade"' % item.url.split('#')[1]
    bloque = scrapertools.find_single_match(data, patron)
    patron = 'class="text-muted">.*?<[^>]+>(.*?)<[^>]+>[^>]+>[^>][^>]+>[^<]+<a href="#" class="slink" id="megadrive-(.*?)" data-link="(.*?)"'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedtitle, scrapedepi, scrapedurl in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedepi = scrapedepi.split('_')[0] + "x" + scrapedepi.split('_')[1].zfill(2)
        scrapedtitle = scrapedepi + scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos_tv",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    return itemlist


def findvideos_tv(item):

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR orange][B]' + videoitem.title + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
"""

