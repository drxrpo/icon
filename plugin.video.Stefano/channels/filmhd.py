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
headers = [['Referer', host]]

# ==============================================================================================================================================

def mainlist(item):
    logger.info("[pureita filmhd] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
             action="fichas",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Per Genere[/COLOR]",
             action="genere",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Per anno[/COLOR]",
             action="genere_years",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Per Paese[/COLOR]",
             action="genere_country",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country2_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - 3D[/COLOR]",
             action="fichas",
             url="%s/genere/3d/" % host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/blueray_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Lista A/Z[/COLOR]",
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

# ==============================================================================================================================================

def genere(item):
    logger.info("[pureita filmhd] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = 'Genere<i class="icon-chevron-down"></i></div>(.*?)</ul>'
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
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================

def genere_years(item):
    logger.info("[pureita filmhd] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = 'Anno<i class="icon-chevron-down"></i></div>(.*?)</ul>'
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

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = 'Nazione<i class="icon-chevron-down"></i></div>(.*?)</ul>'
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
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country2_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================

def genere_az(item):
    logger.info("[pureita filmhd] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = 'ABC<i class="icon-chevron-down"></i></div>(.*?)</ul>'
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
	

    patron = '<div class=".*?">\s*<a href="([^"]+)">\s*'
    patron += '<div class=".*?">\s*<div class=".*?">\s*'
    patron += '(.*?)<img src="([^"]+)"\s*alt="(.*?)">'


    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtv, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if "TV" in scrapedtv else "findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv' if "TV" in scrapedtv else "movie"))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class=\'arrow_pag\'\s*href="([^"]+)">')
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
	

    patron = '<div class=".*?">\s*<a href="([^"]+)">\s*'
    patron += '<div class=".*?">\s*<div class=".*?">\s*'
    patron += '<span class="item-tv">.*?<i></i></span><img src="([^"]+)"\s*alt="(.*?)">'


    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"><span class="fa fa-caret-right"></span>')
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


	




