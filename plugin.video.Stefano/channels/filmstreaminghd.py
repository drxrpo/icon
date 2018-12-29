# -*-  coding: utf-8  -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  filmstreaminghd
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# creato by Robin
# Un grazie a H_2_0 :)
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

__channel__ = "filmstreaminghd"
host = "http://www.filmstreaminghd.biz"
headers = [['Referer', host]]

def mainlist(item):
    logger.info("[streamondemand-pureita filmstreaminghd] mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/guarda/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/genere/animazione/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serie-tv/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==================================================================================================================================================
	
def categorias(item):
    logger.info("[streamondemand-pureita altadefinizione_bid] categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h2>Film per genere</h2(.*?)</ul></div>')

    # Extrae las entradas (carpetas)
    patron = '<li class="cat-item cat-item-\d+"><a href="([^"]+)" >([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita filmstreaminghd] " + item.url + " search " + texto)
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

def peliculas(item):
    logger.info("[streamondemand-pureita filmstreaminghd] peliculas")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<article id=".*?"\s*class="(.*?)">[^>]+>\s*<img src="([^"]+)" alt="([^<]+)">\s*' \
             '<div class="rating">[^h]+href="([^"]+)">.*?' \
	         '<div class="texto">(.*?)</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for type, scrapedthumbnail, scrapedtitle, scrapedurl, scrapedplot in matches:
	
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos_movies" if not "tvshows" in type else "episodios",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR] ",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 show=scrapedtitle,
                 folder=True), tipo='movie' if not "tvshows" in type else "tv"))

    # Extrae el paginador
    patronvideos = '<a class=\'arrow_pag\' href="([^"]+)"><i class=\'icon-caret-right\'></i>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 extra=item.extra,
                 folder=True))

    return itemlist
	
# ==================================================================================================================================================

def peliculas_search(item):
    logger.info("[streamondemand-pureita filmstreaminghd] peliculas_search")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<img\s*src="([^"]+)"[^>]+>\s*<span\s*class="([^<]+)</span>.*?' \
             '<a href="([^"]+)">([^<]+)</a>.*?<p>(.*?)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, genres, scrapedurl, scrapedtitle, scrapedplot  in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos_movies" if not "tvshows" in genres else "episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo="movie" if not "tvshows" in genres else "tv"))

    return itemlist

# ==================================================================================================================================================	

def peliculas_tv(item):
    logger.info("[streamondemand-pureita filmstreaminghd] peliculas_tv")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)" alt="([^<]+)">\s*<div class="rating">[^h]+href="([^"]+)">.*?' \
	         '<div class="texto">(.*?)<\/div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedurl, scrapedplot in matches:
	
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR] ",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = "span class=\"current\">.*?<\/span><a href='([^']+)'[^>]+>"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 extra=item.extra,
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def episodios(item):
    logger.info("[streamondemand-pureita filmstreaminghd] episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="numerando">([^<]+)' \
             '</div><div class="episodiotitle">\s*<a href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedep, scrapedurl, scrapedtitle  in matches:
        scrapedep=scrapedep.replace(" - ", "x")
        scrapedplot = ""
        scrapedthumbnail=""
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos_tv",
                 fulltitle=item.fulltitle,
                 title="[COLOR azure]" + scrapedtitle + " [[COLOR orange]" + scrapedep + "[/COLOR]]",
                 contentType="episode",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 show=scrapedtitle,
                 plot="[COLOR orange]" + item.fulltitle + ": [/COLOR]" + item.plot,
                 folder=True))

    itemlist.reverse()
    return itemlist

# ==================================================================================================================================================

def findvideos_movies(item):
    logger.info("[streamondemand-pureita filmstreaminghd] findvideos_movies")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = '<td><img src="[^=]+=([^.]+).*?"> <a href="([^"]+)" target="_blank">[^<]+</a></td><td>([^<]+)</td>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, quality in matches:

        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle = scrapedtitle.capitalize()
        quality=" [[COLOR yellow]" + quality + "[/COLOR]]"
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 fulltitle=item.title,
                 title="[COLOR azure]" + item.title + " [[COLOR orange]" + scrapedtitle + "[/COLOR]]" + quality,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 show=item.show,
                 plot=item.plot,
                 folder=True))
				 
    data = httptools.downloadpage(item.url).data
    patron = '<h2 class="tabtitle">([^<]+)<\/h2><div class[^>]+><p><iframe\s*src="([^"]+)"[^>]+></iframe>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle = scrapedtitle.capitalize()
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 fulltitle=item.title,
                 title="[COLOR azure]" + item.title + " [[COLOR orange]" + scrapedtitle + "[/COLOR]]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 show=item.show,
                 plot=item.plot,
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def findvideos_tv(item):
    logger.info("[streamondemand-pureita filmstreaminghd] findvideos_tv")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<p><iframe\s*src="([^"]+)"[^>]+></iframe>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        data += httptools.downloadpage(scrapedurl).data
		
    for videoitem in servertools.find_video_items(data=data):
        videoitem.title = item.title + " [COLOR orange]" + videoitem.title + "[/COLOR]"
        videoitem.fulltitle = item.title
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
        itemlist.append(videoitem)

		
    return itemlist
	
# ==================================================================================================================================================
	
def play(item):
    logger.info("[streamondemand-pureita filmstreaminghd] play")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        data += httptools.downloadpage(scrapedurl).data
		
    for videoitem in servertools.find_video_items(data=data):
        videoitem.title = item.fulltitle + " [COLOR orange]" + videoitem.title + "[/COLOR]"
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
        itemlist.append(videoitem)
	
    return itemlist