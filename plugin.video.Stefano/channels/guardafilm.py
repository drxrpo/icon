# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA / XBMC Plugin
# Canale GuardaFilm
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "guardafilm"
host = "http://www.guardafilm.top"

headers = [['Referer', host]]



def mainlist(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] mainlist")
    itemlist = [Item(channel=__channel__,
                     action="peliculas_update",
                     title="Film [COLOR orange] - Novita[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     action="genere_top",
                     title="Film [COLOR orange] - Categorie TOP[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="genere",
                     title="Film [COLOR orange] - Categorie Archivio[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="peliculas_animation",
                     title="Film [COLOR orange] - Animazione [/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ===================================================================================================================================================

def search(item, texto):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] search")

    item.url = host + "/?s=" + texto

    try:
        return peliculas_update(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ===================================================================================================================================================

def genere(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, r'<div\s*class="row"><div\s*class="col-sm-3">([^+]+)<\/span><\/form><\/div>')
	
    patron = r'<a\s*href="[^"]+"\s*title[^>]+>([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedtitle in matches:

        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_genre",
                 title=scrapedtitle,
                 url=host,			 
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist
	
# ===================================================================================================================================================

def genere_top(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] genere_top")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, r'<div\s*class="row"><div\s*class="col-sm-3">([^+]+)<\/span><\/form><\/div>')
	
    patron = r'<a\s*href="([^"]+)"\s*title[^>]+>([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_top",
                 title=scrapedtitle,
                 url=scrapedurl,			 
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist
	
# ===================================================================================================================================================

def peliculas_update(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] peliculas_update")
    itemlist = []
    PERPAGE = 14
	
    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)
	
    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a\s*href="([^"]+)"[^>]+>\s*<img[^>]+alt="locandina([^<]+)"\s*src="([^"]+)"\s*\/>'

    matches = re.compile(patron, re.DOTALL).findall(data)


    for i, (scrapedurl, scrapedtitle, scrapedthumbnail) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle +  "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_update",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ===================================================================================================================================================

def peliculas_top(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] peliculas_top")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div\s*class="col-xs-6 col-sm-2-5">\s*<a\s*href="([^"]+)"[^>]+>\s*'
    patron += '<img\s*class[^>]+alt="locandina\s*([^<]+)"\s*src="([^"]+)"\s*\/>'
    matches = re.compile(patron, re.DOTALL).findall(data)
	
    for scrapedurl,  scrapedtitle, scrapedthumbnail in matches:
        scrapedurl = host + scrapedurl
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo="movie"))
				 
    next_page = scrapertools.find_single_match(data, "")
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_top",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist


# ===================================================================================================================================================

def peliculas_animation(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] peliculas_animation")
    itemlist = []
    PERPAGE = 14
	
    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)
	
    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, 'Animazione</h2></div></div></div></div>(.*?)</h2></div></div></div></div>')

    # Extrae las entradas (carpetas)
    patron = '<div\s*style=".*?"\s*class=".*?" meta-title="[^<]+">\s*<a\s*'
    patron += 'href="([^"]+)" class=".*?">\s*<img\s*'
    patron += 'class[^>]+src="([^"]+)" />.*?'
    patron += '<p\s*class="strongText">([^<]+)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)


    for i, (scrapedurl, scrapedthumbnail, scrapedtitle) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle +  "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_animation",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ===================================================================================================================================================
	
def peliculas_genre(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] peliculas_genre")
    itemlist = []

	
    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, item.title +'</h2></div></div></div></div>(.*?)</h2></div></div></div></div>')

    # Extrae las entradas (carpetas)
    patron = '<div\s*style=".*?"\s*class=".*?" meta-title="[^<]+">\s*<a\s*'
    patron += 'href="([^"]+)" class=".*?">\s*<img\s*'
    patron += 'class[^>]+src="([^"]+)" />.*?'
    patron += '<p\s*class="strongText">([^<]+)</p>'

    matches = re.compile(patron, re.DOTALL).findall(blocco)


    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle +  "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    return itemlist
	
# ===================================================================================================================================================
	
"""
def findvideos(item):
    logger.info("[StreamOnDemand-PureITA GuardaFilm] findvideos")
    itemlist = []
	
    data = httptools.downloadpage(item.url, headers=headers).data 
    patron = 'src="([^"]+)" frameborder="0"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        if "dir?" in scrapedurl:
            data += httptools.downloadpage(scrapedurl).url
        else:
            data += httptools.downloadpage(scrapedurl).data

    for videoitem in servertools.find_video_items(data=data):
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
        itemlist.append(videoitem)

    return itemlist
"""




