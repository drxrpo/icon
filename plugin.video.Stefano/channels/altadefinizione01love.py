# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  Altadefinizione01Love
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

__channel__ = "altadefinizione01love"
host = "http://www.altadefinizione01.zone/"
headers = [['Referer', host]]

def isGeneric():
    return True


def mainlist(item):
    logger.info("[streamondemand-pureita altadefinizione01love] mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Cinema[/COLOR]",
                     action="peliculas",
                     url="%s/cinema/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Novita'[/COLOR]",
                     action="peliculas_update",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Attori consigliati[/COLOR]",
                     action="actors_list",
                     url="%s/attori/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_actors_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Lista[/COLOR]",
                     action="peliculas_list",
                     url="%s/catalog/a/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/all_movies_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- A-Z[/COLOR]",
                     action="list_az",
                     url="%s/catalog/a/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/all_movies_P.png"),
               Item(channel=__channel__,
                     title="[COLOR orange]Cerca Film...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def categorias(item):
    logger.info("[streamondemand-pureita altadefinizione01love] categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<ul class="kategori_list">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        if "Altadefinizione01" in scrapedtitle: 
		    continue
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def list_az(item):
    logger.info("[streamondemand-pureita altadefinizione01love] list_az")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data


    # Extrae las entradas (carpetas)
    patron = '<a title=".*?" href="([^"]+)"><span>([^<]+)</span></a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png",
                 folder=True))

    return itemlist
	
# ==============================================================================================================================================================================

def actors_list(item):
    logger.info("[streamondemand-pureita altadefinizione01love] actors_list")
    itemlist = []
    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<h2>Attori consigliati su Altadefinizione01:</h2>(.*?)</div></div>'
	
    data = scrapertools.find_single_match(data, patron)
              
    patron = '<a href="([^"]+)" title="[^>]+">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_actors_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_list(item):
    logger.info("[streamondemand-pureita altadefinizione01love] peliculas_list")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img\s*[^>]+src="([^"]+)[^>]+>\s*</a>\s*</td>\s*[^>]+>'
    patron += '<h2>\s*<a href="([^"]+)"\s*title=".*?">([^<]+)</a>\s*</h2></td>.*?'
    patron += '<td class="mlnh-4">(.*?)</td>.*?<td class="mlnh-6"><span class="label">(.*?)</span>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        rating = scrapertools.unescape(match.group(5))
        quality = scrapertools.unescape(match.group(4))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = scrapertools.unescape(match.group(2))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(1))
        info_video = " [[COLOR yellow]" + quality + "[/COLOR]]" + " [[COLOR yellow]" + rating + "[/COLOR]]"
		
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + info_video,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = 'href="([^"]+)">&raquo;</a></i>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])

        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_list",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================	

def peliculas_update(item):
    logger.info("[streamondemand-pureita altadefinizione01love] peliculas_update")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="slider-strip"></div>(.*?)<div id="right_bar">'
    data = scrapertools.find_single_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<div class="imdb_bg">(.*?)</div>\s*</div>\s*<a href="([^"]+)">\s*' \
             '<img width=".*?"\s*height=".*?" src="([^"]+)" [^>]+ alt="([^<]+)"\s*title="".*?/>.*?' \
             '</a>\s*<div class="trdublaj">\s*(.*?)</div>\s*[^>]+>(.*?)\s*<'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        sub = scrapertools.unescape(match.group(6))
        quality = scrapertools.unescape(match.group(5))
        scrapedtitle = scrapertools.unescape(match.group(4))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(3))
        scrapedurl = scrapertools.unescape(match.group(2))
        rating = scrapertools.unescape(match.group(1))
        info_video = "[[COLOR yellow]" + quality + "[/COLOR]] " + sub + " [[COLOR yellow]" + rating + "[/COLOR]]"
         
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR] " + info_video,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = 'href="([^"]+)">&raquo;</a></i>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_update",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================	
		
def peliculas(item):
    logger.info("[streamondemand-pureita altadefinizione01love] peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<h2> <a href="([^"]+)">([^"]+)</a>\s*</h2>\s*<div class="imdb_bg">([^<]+)</div>\s*'
    patron += '</div>\s*<a href[^>]+>[^>]+src="([^"]+)"[^>]+>\s*</a>\s*'
    patron += '<div class="trdublaj">\s*(.*?)</div>\s*[^>]+>(.*?)\s*<'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        sub = scrapertools.unescape(match.group(6))
        quality = scrapertools.unescape(match.group(5))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(4))
        rating = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = scrapertools.unescape(match.group(1))
        info_video = "[[COLOR yellow]" + quality + "[/COLOR]] " + sub + " [[COLOR yellow]" + rating + "[/COLOR]]"

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR] " + info_video,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = 'href="([^"]+)">&raquo;</a></i>'
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
	
def findvideos(item):
    logger.info("[streamondemand-pureita altadefinizione01love] findvideos")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '</a>\s*<a href="[^>]+" data-link="([^"]+)">\s*<li class="part">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        if not "http:" in scrapedurl:
          scrapedurl = "http:" + scrapedurl
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
	
# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita altadefinizione01love] " + item.url + " search " + texto)
    item.url = host + "/?do=search&subaction=search&story=" + texto
    try:
        return peliculas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================


