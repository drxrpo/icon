# -*- coding: utf-8 -*-
# ==============================================================
# streamondemand-PureITA / XBMC Plugin
# Canale ffilm
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ==============================================================

import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "ffilms"
host = "https://ffilms.org/italiano/"

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'],
           ['Accept-Encoding', 'gzip, deflate'],
           ['Referer', host]]


# ==================================================================================================================================================

def mainlist(item):
    logger.info("[streamondemand-pureita ffilm] mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra=" Ultimi",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Popolari[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra=" Popolarità",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Raccomandati[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra=" Mi piace",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Per Anno[/COLOR]",
                     action="categorias_year",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Cerca ...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==================================================================================================================================================

def categorias(item):
    logger.info("[streamondemand-pureita ffilm] categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<ul id="menu-cat" class[^>]+>(.*?)</ul>\s*</nav>\s*</div>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)\s*<'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:

        scrapedplot = ""
        scrapedthumbnail = ""
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_src",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def categorias_year(item):
    logger.info("[streamondemand-pureita ffilm] categorias_year")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, 'Anni(.*?)Ultimi</h3>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)"\s*class=".*?"\s*style=".*?"\s*aria-label[^>]+>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        year="[COLOR azure]Anni:[COLOR orange] '[/COLOR]"
        num=0
        for i in scrapedtitle:
              if(i.isdigit()):
                    num=num+1
        if num > 3:
          year='[COLOR azure]Anno:[/COLOR] '
        scrapedplot = ""
        scrapedthumbnail = ""
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_src",
                 title=year + "[COLOR orange][I]" + scrapedtitle + "[/I][/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita ffilm] search")
    item.url = host + "/?s=" + texto
    try:
        return peliculas_src(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==================================================================================================================================================

def peliculas_src(item):
    logger.info("[streamondemand-pureita ffilm] peliculas_search")
    itemlist = []
	
    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
	
    # Extrae las entradas (carpetas)
    patron = 'src="([^"]+)"\s*class[^>]+></a>.*?'
    patron += '<h3><a href="([^"]+)">([^<]+)</a></h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle = scrapedtitle.replace("’", "'").replace("- ", "")
        scrapedtitle = scrapedtitle.replace(" Gratis", "").replace(" in Italiano", "")
        scrapedtitle = scrapedtitle.replace(" Guarda", "").replace(" Italiano", "")
        scrapedtitle = scrapedtitle.replace(" Streaming", "").replace(" Ita", "")
        scrapedtitle = scrapedtitle.replace(" Film Completo", "")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="movie",
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie"))

    # Extrae el paginador
    patronvideos = '<li><a class="next page-numbers" href="([^"]+)">Next.*?</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_src",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================

def peliculas(item):
    logger.info("[streamondemand-pureita ffilm] peliculas")
    itemlist = []
    minpage = 14
	
    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)	
	
    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, r'<h3><i class="fa fa-play"></i>%s</h3>(.*?)</div>\s*</div>\s*</div>\s*</div>' % item.extra)
	
    # Extrae las entradas (carpetas)
    patron = '<a title="([^"]+)" href="([^"]+)"><img.*?src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for i, (scrapedtitle, scrapedurl, scrapedthumbnail) in enumerate (matches):
        if (p - 1) * minpage > i: continue
        if i >= p * minpage: break

        scrapedplot = ""
        scrapedtitle = scrapedtitle.replace("’", "'").replace("- ", "")
        scrapedtitle = scrapedtitle.replace(" Gratis", "").replace(" in Italiano", "")
        scrapedtitle = scrapedtitle.replace(" Guarda", "").replace(" Italiano", "")
        scrapedtitle = scrapedtitle.replace(" Streaming", "").replace(" Ita", "")
        scrapedtitle = scrapedtitle.replace(" Film Completo", "")
		
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
    if len(matches) >= p * minpage:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
	
# ==================================================================================================================================================

def findvideos(item):
    logger.info("[streamondemand-pureita ffilm] findvideos")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = r'<li(?: class="active"| )><a href="([^"]+)">\d+</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl in matches:
        data = scrapertools.anti_cloudflare(scrapedurl, headers)
        videos = servertools.find_video_items(data=data)
        for video in videos:
            itemlist.append(video)

    for videoitem in itemlist:
        servername = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = item.title + " [[COLOR orange]" + servername.capitalize() + "[/COLOR]]" 
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
    return itemlist

# ==================================================================================================================================================

