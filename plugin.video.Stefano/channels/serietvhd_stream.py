# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale serietvhd_stream
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

__channel__ = "serietvhd_stream"
host = "https://serietvhd.stream/"
headers = [['Referer', host]]

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand-pureita [serietvhd_stream mainlist]")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Top IMDB[/COLOR]",
                     action="peliculas_imdb",
                     url="%s/top-imdb/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_new.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Categorie[/COLOR]",
                     action="genere",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Lista[/COLOR]",
                     action="peliculas_list",
                     url="%s/serietv/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Popolari[/COLOR]",
                     action="popular_list",
                     url="%s/piu-popolari/" %host,
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
    logger.info("[streamondemand-pureita serietvhd_stream] " + item.url + " search " + texto)

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
    logger.info("streamondemand-pureita [serietvhd_stream peliculas_search]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)"\s*alt="(.*?)"\s*/>.*?'
    patron += '<span class="rating">([^"]+)</span>.*?'
    patron += '<div class="contenido"><p>(.*?)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, rating, scrapedplot  in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle + " " + '([COLOR yellow]' + rating + '[/COLOR])',
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    return itemlist		

# ==============================================================================================================================================================================		

def genere(item):
    logger.info("streamondemand-pureita [serietvhd_stream genere]")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<li id="menu-item-.*?" class="menu-item menu-item-type-taxonomy menu-item-object-genres menu-item-.*?">'
    patron += '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

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

def peliculas(item):
    logger.info("streamondemand-pureita [serietvhd_stream peliculas]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="poster">\s*<img src="([^"]+)" \s*alt="([^"]+)">\s*'
    patron += '<div[^>]+>[^>]+></span>\s*(.*?)<\/div>\s*[^>]+>\s*[^>]+>.*?'
    patron += '<a href="([^"]+)">[^>]+></div></a></div><div class="data"><h3>.*?'
    patron += '<div class="texto">(.*?)</div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, rating, scrapedurl, scrapedplot in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle + " " + '([COLOR yellow]' + rating + '[/COLOR])',
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"><span class="icon-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_list(item):
    logger.info("streamondemand-pureita [serietvhd_stream peliculas_list]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h1>Serie TV</h1>(.*?)<h2>Genere</h2>')	
	
    patron = '<div class="poster">\s*<img src="([^"]+)" \s*alt="([^"]+)">\s*'
    patron += '<div[^>]+>[^>]+></span>\s*(.*?)<\/div>\s*[^>]+>\s*[^>]+>.*?'
    patron += '<a href="([^"]+)">[^>]+></div></a></div><div class="data"><h3>.*?'
    patron += '<div class="texto">(.*?)</div>'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedthumbnail, scrapedtitle, rating, scrapedurl, scrapedplot in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle + " " + '([COLOR yellow]' + rating + '[/COLOR])',
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"><span class="icon-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================
	
def peliculas_imdb(item):
    logger.info("streamondemand-pureita [serietvhd_stream peliculas_imdb]")
    itemlist = []
    PERPAGE = 14

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas
    patron = '<img src="([^"]+)"\s*/>'
    patron += '</a></div></div><div class="puesto">([^"]+)</div><div class="rating">([^"]+)</div>'
    patron += '<div class="title"><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedthumbnail, position, rating, scrapedurl, scrapedtitle ) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
                 title="[COLOR red]" + position + "-" +" [COLOR azure]" + scrapedtitle + " [[COLOR yellow]" + rating + "[/COLOR]]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=item.plot,
                 folder=True), tipo="tv"))
				 
    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_imdb",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
	
# ==============================================================================================================================================================================

def popular_list(item):
    logger.info("streamondemand-pureita [serietvhd_stream peliculas]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<img src="([^"]+)"\s*alt="[^>]+"><div class="rating"><span class=".*?"><\/span>\s*([^"]+)</div><div class="mepo">'
    patron += '</div>\s*<a href="([^"]+)"><div class="see"></div></a><\/div><div class="data"><h3>\s*<a href="[^>]+>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, rating, scrapedurl, scrapedtitle in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle + " [[COLOR yellow]" + rating + "[/COLOR]]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv'))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, 'a href="([^"]+)"><span class="icon-chevron-right"></span>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="popular_list",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================
	
def episodios(item):
    logger.info("streamondemand-pureita [serietvhd_stream episodios]")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="numerando">(.*?)</div><div class="episodiotitle">\s*<a href="([^"]+)">(.*?)</a>.*?img src="([^"]+)"></a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedep, scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        if "Episodio"  in scrapedtitle or "Episode" in scrapedtitle or "Cassetta" in scrapedtitle:
		      scrapedtitle=item.title
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle + "[COLOR orange]" + " Episodio " + scrapedep + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=item.plot,
                 show=scrapedtitle), tipo='serie'))


    return itemlist

# ==============================================================================================================================================================================	
		
def findvideos(item):
    logger.info("streamondemand-pureita [serietvhd_stream  findvideos]")
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



