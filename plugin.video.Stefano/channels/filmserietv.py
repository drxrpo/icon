# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale filmserietv
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

__channel__ = "filmserietv"
host = "http://filmserietv.stream"
headers = [['Referer', host]]

def isGeneric():
    return True

def mainlist(item):
    logger.info("[streamondemand-pureita filmserietv] mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film & Serie TV[COLOR orange] - Popolari[/COLOR]",
                     action="popular_list",
                     url="%s/popolari/" %host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/movies/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Anno[/COLOR]",
                     action="categorias_year",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Top IMDB[/COLOR]",
                     action="peliculas_imdb",
                     url="%s/top-imdb/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas_list",
                     url="http://filmserietv.stream/tvshows/",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca ...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita filmserietv] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return peliculas_search(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==================================================================================================================================================

def peliculas_search(item):
    logger.info("[streamondemand-pureita filmserietv] peliculas_search")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)"\s*alt="(.*?)"\s*/>'
    patron += '<span class="([^"]+)">[^<]+</span>.*?'
    patron += '<span class[^>]+>([^<]+)</span>.*?<p>(.*?)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, genre, rating, scrapedplot  in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if "tvshows" in genre else "findvideos",
                 title=scrapedtitle + " " + '([COLOR yellow]' + rating + '[/COLOR])',
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv' if "tvshows" in genre else "movie"))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, "<span class=\"current\">\d+</span><a href='([^']+)' class=\"inactive\">\d+</a>")
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_search",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist	

# ==================================================================================================================================================		

def categorias(item):
    logger.info("[streamondemand-pureita filmserietv] categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, 'Genere</a>(.*?)Anno</a><ul class="sub-menu">')	

    # Extrae las entradas (carpetas)
    patron = '<a\s*href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 extra="movie",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================

def categorias_year(item):
    logger.info("[streamondemand-pureita filmserietv] categorias_year")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, 'Anno</a>(.*?)</li></ul></li>')	

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 extra="movie",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================

def peliculas(item):
    logger.info("[streamondemand-pureita filmserietv] peliculas")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="poster">\s*<img src="([^"]+)" \s*alt="([^"]+)">\s*'
    patron += '<div[^>]+>[^>]+><\/span>\s*([^<]+)<\/div>\s*[^>]+>\s*[^>]+>([^<]+)<\/span>.*?'
    patron += '<a href="([^"]+)">[^>]+></div></a></div><div class="data"><h3>.*?'
    patron += '<div class="texto">(.*?)</div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, rating, quality, scrapedurl, scrapedplot in matches:
        if rating == "0":
           rating =""
        else:
           rating = " [[COLOR yellow]" + rating + "[/COLOR]]"
        quality = " [[COLOR yellow]" + quality + "[/COLOR]]"

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if not "serie" in item.extra else "episodios",
                 title=scrapedtitle + rating + quality,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie' if not "serie" in item.extra else "tv"))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, '<a class=\'arrow_pag\' href="([^"]+)"><i id=\'nextpagination\' class=\'icon-caret-right\'>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================

def peliculas_list(item):
    logger.info("[streamondemand-pureita filmserietv] peliculas_list")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

	
    patron = '<div class="poster">\s*<img src="([^"]+)" \s*alt="([^"]+)">\s*'
    patron += '<div[^>]+>[^>]+><\/span>\s*([^<]+)<\/div>\s*[^>]+>\s*[^>]+>\s*'
    patron += '<a href="([^"]+)">[^>]+><\/div><\/a><\/div><div class="data"><h3>.*?'
    patron += '<div class="texto">(.*?)<\/div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, rating, scrapedurl, scrapedplot in matches:
        if rating == "0":
           rating =""
        else:
           rating = " ([COLOR yellow]" + rating + "[/COLOR])"
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, "<span class=\"current\">\d+</span><a href='([^']+)' class=\"inactive\">\d+</a>")
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================
	
def peliculas_imdb(item):
    logger.info("[streamondemand-pureita filmserietv] peliculas_imdb")
    itemlist = []
    PERPAGE = 14

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '<h3>Serie Tv</h3>(.*?)<h2>Genere</h2>')
	
    # Extrae las entradas
    patron = '<img src="([^"]+)"\s*/>'
    patron += '</a></div></div><div class="puesto">([^"]+)</div><div class="rating">([^"]+)</div>'
    patron += '<div class="title"><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for i, (scrapedthumbnail, position, rating, scrapedurl, scrapedtitle ) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
                 title="[COLOR red]" + position + "-" +" [COLOR azure]" + scrapedtitle + " [[COLOR yellow]" + rating + "[/COLOR]]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 plot=scrapedplot,
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
	
# ==================================================================================================================================================

def popular_list(item):
    logger.info("[streamondemand-pureita filmserietv] popular_list")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="poster">\s*<img src="([^"]+)" \s*alt="([^"]+)">\s*<div[^>]+>[^>]+>'
    patron += '<\/span>\s*([^<]+)<\/div>\s*[^>]+>\s*[^>]+>(.*?)<.*?a href="([^"]+)">[^>]+><\/div><\/a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, rating, quality, scrapedurl in matches:
        if rating=="0":
           rating =""
        else:
           rating = " ([COLOR yellow]" + rating + "[/COLOR])"

        if quality:
         quality = " ([COLOR yellow]" + quality + "[/COLOR])"
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if not "tvshows" in scrapedurl else "episodios",
                 title=scrapedtitle + rating + quality,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie' if not "tvshows" in scrapedurl else "episodios"))

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"\s*><span class="icon-chevron-right"></span>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="popular_list",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================
	
def episodios(item):
    logger.info("[streamondemand-pureita filmserietv] episodios")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="numerando">(.*?)</div><div class="episodiotitle">\s*<a href="([^"]+)">(.*?)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedep, scrapedurl, scrapedtitle in matches:
        if "Episodio"  in scrapedtitle or "Episode" in scrapedtitle \
         or "Cassetta" in scrapedtitle or "--" in scrapedtitle:
		      scrapedtitle=item.fulltitle
        scrapedep=scrapedep.replace(" - --", "")
        scrapedep=scrapedep.replace(" - ", "x")
        scrapedep = "  ([COLOR orange]" + scrapedep + "[/COLOR])"
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle + scrapedep,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 fulltitle=item.fulltitle,
                 plot="[COLOR orange]" + item.fulltitle + "[/COLOR] - " + item.plot,
                 show=item.show), tipo='serie'))


    return itemlist

# ==================================================================================================================================================	
		
def findvideos(item):
    logger.info("[streamondemand-pureita filmserietv]  findvideos")
    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.title = "".join(['[COLOR azure]' + item.title  + '  [COLOR orange]' + server + '[/COLOR]'])
        videoitem.fulltitle = item.title + videoitem.title
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

        

