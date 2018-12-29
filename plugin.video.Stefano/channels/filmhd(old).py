# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale FilmHD
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

__channel__ = "filmhd"

host = "http://filmhd.me"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host],
    ['Cache-Control', 'max-age=0']
]


def isGeneric():
    return True

# ==============================================================================================================================================

def mainlist(item):
    logger.info("[pureita filmhd] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Novita'[/COLOR]",
             action="fichas",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Per Genere[/COLOR]",
             action="genere",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Per anno[/COLOR]",
             action="genere_years",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Per Paese[/COLOR]",
             action="genere_country",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country2_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]3D[/COLOR]",
             action="fichas",
             url="%s/genere/3d/" % host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/blueray_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]A-Z[/COLOR]",
             action="genere_az",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Serie TV[/COLOR]",
             action="fichas_tv",
             url=host + "/genere/serie-tv/",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
        Item(channel=__channel__,
             title="[COLOR orange]Cerca...[/COLOR]",
             action="search",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================

def genere(item):
    logger.info("[pureita filmhd] genere")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<li class="dropdown genre-filter">(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a href="([^"]+)">([^<]+)</a></label>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================

def genere_years(item):
    logger.info("[pureita filmhd] genere")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<div class="dropdown-toggle" data-toggle="dropdown">Anno<i class="icon-chevron-down"></i></div>(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================

def genere_country(item):
    logger.info("[pureita filmhd] genere")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<div class="dropdown-toggle" data-toggle="dropdown">Nazione<i class="icon-chevron-down"></i></div>(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="(.*?)\s*">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country2_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================

def genere_az(item):
    logger.info("[pureita filmhd] genere")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<li class="dropdown abc-filter">(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li class="abc"><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================

def fichas(item):
    logger.info("[pureita filmhd] fichas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	

    patron = '<div class=".*?"><i style=".*?">(.*?)</i></div>\s*</div>\s*<a href="([^"]+)">\s*'
    patron += '<div class="movie-play">\s*<i class="icon-controller-play"></i>\s*'
    patron += '</div>\s*<img src="([^"]+)".*?>\s*</a>\s*</div>\s*[^>]+>\s*<h2 class="movie-title">([^<]+)</h2>'


    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtv, scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)


        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if "TV" in scrapedtv else "findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv' if "TV" in scrapedtv else "movie"))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="nextpostslink" href="([^"]+)">»</a>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================

def fichas_tv(item):
    logger.info("[pureita filmhd] fichas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	

    patron = '<a href="([^"]+)">\s*<div class="movie-play">\s*<i class="icon-controller-play">'
    patron += '</i>\s*</div>\s*<img src="([^"]+)" alt="([^<]+)">'


    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="nextpostslink" href="([^"]+)">»</a>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================
	
def episodios(item):
    logger.info("streamondemand.channels.altadefinizionezone episodios")

    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data


    patron = "#openload(.*?) span[^>]+src='[^>]+' frameborder[^>]+><\/iframe><p\s*"
    patron += "id='buttondownload'><a\s*href='([^<]+)' rel='nofollow' target='_blank'>" 
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapedtitle.replace("_", " X ")


        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))

    return itemlist

	
# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("[pureita filmhd] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return fichas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


	




