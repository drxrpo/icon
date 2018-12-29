# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale FilmStreamingGratis
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

__channel__ = "filmstreaminggratis"
host = "http://www.filmstreaminggratis.org"

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0'],
           ['Accept-Encoding', 'gzip, deflate'],
           ['Referer', host]]


def mainlist(item):
    logger.info("streamondemand-pureita.filmstreaminggratis mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]Aggiornati[/COLOR]",
                     action="peliculas_movie",
                     url="%s/nuovi/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]Animazione[/COLOR]",
                     action="peliculas_movie",
                     url="%s/animazione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange]- Categorie[/COLOR]",
                     action="categorias",
                     url="%s/nuovi/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]Archivio[/COLOR]",
                     action="peliculas_movie",
                     url="%s/blog/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ========================================================================================================================================================

def search(item, texto):
    logger.info("streamondemand-pureita.filmstreaminggratis search")
    item.url = host + "/?s=" + texto
    try:
        return peliculas_movie(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# ========================================================================================================================================================

def categorias(item):
    logger.info("[streamondemand-pureita videotecaproject] serie_az")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, 'Film Streaming Categorie</h3>(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)" title[^>]+>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_movie",
                 fulltitle=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ========================================================================================================================================================
	
def peliculas_movie(item):
    logger.info("[streamondemand-pureita filmstreaminggratis] peliculas_srcmovie")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
	
    # Extrae las entradas (carpetas)
    patron = '<figure class[^>]+><a href="([^"]+)" title="(.*?)"\s*>'
    patron += '<img src[^>]+data-src="([^"]+)"[^>]+><\/a><\/figure>'
    patron += '.*?<div class="excerpt">\s*(.*?)<\/div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedplot in matches:
        scrapedplot=scrapedplot.replace('[tabby title=', '').replace('Openload', '').replace('Streamango', '')
        scrapedplot=scrapedplot.replace('-Stream', '').replace('[tabbyending]', '').replace('"', '').replace(']', '')
        scrapedplot=scrapedplot.strip()
        if "serie-tv" in scrapedurl:
          continue

        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">Successivo</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_movie",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))
   
    return itemlist
	
# ========================================================================================================================================================

def findvideos(item):
    logger.info("streamondemand-pureita.filmstreaminggratis findvideos")
    itemlist = []
	
    data = scrapertools.anti_cloudflare(item.url, headers)

    blocco = scrapertools.get_match(data, r'<br />(.*?)</div></div>')
    patron = r'.*?src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl in matches:
        data = scrapertools.anti_cloudflare(scrapedurl, headers)
        videos = servertools.find_video_items(data=data)
        for video in videos:
            itemlist.append(video)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[[COLOR orange]%s[/COLOR]] " % server, item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
		
    return itemlist

# ========================================================================================================================================================





