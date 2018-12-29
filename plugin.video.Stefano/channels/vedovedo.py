# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale vedovedo
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

__channel__ = "vedovedo"
host = "https://vedovedo.com"
headers = [['Referer', host]]


def mainlist(item):
    logger.info("streamondemand-pureita [vedovedo mainlist]")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas_tv",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_new.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Categorie[/COLOR]",
                     action="genere",
                     url="%s/categorie/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Lista[/COLOR]",
                     action="peliculas_archive",
                     url="%s/serie-tv-streaming-ita/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Ultime Inserite[/COLOR]",
                     action="peliculas_new",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita vedovedo] " + item.url + " search " + texto)

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
    logger.info("streamondemand-pureita [vedovedo peliculas_search]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<a href="([^"]+)" rel="bookmark">([^<]+)</a></h2>.*?src="([^"]+)"[^>]+>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail  in matches:
        scrapedtitle = scrapedtitle.replace("Streaming ITA", "")
        scrapedtitle = scrapedtitle.replace("Serie TV", "")
        scrapedtitle = scrapedtitle.replace("&#8211;", "")
        scrapedtitle = scrapedtitle.replace("&#8217;", "")
        scrapedtitle = scrapedtitle.replace("  ", "")
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title='[COLOR azure]' + scrapedtitle + '[/COLOR]',
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    return itemlist		

# ==============================================================================================================================================================================		

def genere(item):
    logger.info("streamondemand-pureita [vedovedo genere]")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<li class="cat-item cat-item-\d+"><a href="([^"]+)"\s*>([^<]+)</a>'
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

def peliculas_tv(item):
    logger.info("streamondemand-pureita [vedovedo peliculas_tv]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<a title[^>]+href\s*="([^"]+)"><img\s*alt=".*?"\s*title="([^"]+)"\s*'
    patron += 'class="img-responsive"\s*src="([^"]+)"></a></div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapedtitle.replace("Streaming ITA", "")
        scrapedtitle = scrapedtitle.replace("Serie TV", "")
        scrapedtitle = scrapedtitle.replace("&#8211;", "")
        scrapedtitle = scrapedtitle.replace("&#8217;", "")
        scrapedtitle = scrapedtitle.replace("  ", "")
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)"><i class="fa fa-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_list(item):
    logger.info("streamondemand-pureita [vedovedo peliculas_list]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<a\s*href="([^"]+)"\s*title="[^>]+">([^>]+)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace("Streaming ITA", "")
        scrapedtitle = scrapedtitle.replace("Serie TV", "")
        scrapedtitle = scrapedtitle.replace("&#8211;", "")
        scrapedtitle = scrapedtitle.replace("&#8217;", "")
        scrapedtitle = scrapedtitle.replace("  ", "")
        scrapedplot = ""
        scrapedthumbnail = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================
	
def peliculas_archive(item):
    logger.info("streamondemand-pureita [vedovedo peliculas_archive]")
    itemlist = []
    PERPAGE = 14

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas
    patron = '<a\s*title=".*?" class="title" href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedurl, scrapedtitle ) in enumerate(matches):
        scrapedtitle = scrapedtitle.replace("Streaming ITA", "")
        scrapedtitle = scrapedtitle.replace("Serie TV", "")
        scrapedtitle = scrapedtitle.replace("&#8211;", "")
        scrapedtitle = scrapedtitle.replace("&#8217;", "")
        scrapedtitle = scrapedtitle.replace("  ", "")

        scrapedplot = ""
        scrapedthumbnail = ""
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo="tv"))
				 
    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_archive",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
	
# ==============================================================================================================================================================================

def peliculas_new(item):
    logger.info("streamondemand-pureita [serietvhd_stream peliculas_list]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, 'Nuovi Film &#038; Serie</h2>(.*?)</ul></div></section>')	
	
    patron = '<a title="([^"]+)" href="([^"]+)" target="_blank">'
    patron += '<img width[^>]+src="([^"]+)" class[^>]+>.*?<div class="rpwwt-post-excerpt">(.*?)</div>'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedtitle, scrapedurl, scrapedthumbnail, scrapedplot in matches:
        scrapedtitle = scrapedtitle.replace("Streaming ITA", "")
        scrapedtitle = scrapedtitle.replace("Serie TV", "")
        scrapedtitle = scrapedtitle.replace("&#8211;", "")
        scrapedtitle = scrapedtitle.replace("&#8217;", "")
        scrapedtitle = scrapedtitle.replace("  ", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title='[COLOR azure]' + scrapedtitle + '[/COLOR]',
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))


    return itemlist

# ==============================================================================================================================================================================
	
def episodios(item):
    logger.info("streamondemand-pureita [vedovedo episodios]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<span class="prev[^\d+]+>([^<]+)</.*?>'
    patron += '<a class="blue-link" href="([^"]+)" target="_blank" rel="noopener">[^<]+</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapedtitle.replace("&#8211;", "")
        scrapedtitle = scrapedtitle.replace("&#8217;", "")

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 fulltitle=scrapedtitle,
                 plot=item.plot,
                 show=scrapedtitle), tipo='serie'))

    return itemlist

# ==============================================================================================================================================================================	
		
def findvideos(item):
    logger.info("streamondemand-pureita [vedovedo  findvideos]")
    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR orange]' + videoitem.title + '[/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist



