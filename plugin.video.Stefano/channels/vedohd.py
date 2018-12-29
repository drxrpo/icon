# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale vedohd
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import base64
import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "vedohd"
host = "http://vedohd.stream/"
headers = [['Referer', host]]



def mainlist(item):
    logger.info("[streamondemand-pureita vedohd] mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url="%s//film-hd/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Top Imdb[/COLOR]",
                     action="peliculas_imdb",
                     url="%s/top-imdb/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
	            Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Popolari[/COLOR]",
                     action="peliculas",
                     url="%s/trending/?get=movies" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Raccomandati[/COLOR]",
                     action="peliculas",
                     url="%s/ratings/?get=movies" %host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="genere",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Anno[/COLOR]",
                     action="year",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ========================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita vedohd]] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return peliculas_search(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ========================================================================================================================================================

def peliculas_search(item):
    logger.info("[streamondemand-pureita vedohd] peliculas_search")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)"\s*alt="(.*?)"\s*\/>[^>]+>(.*?)<\/span>.*?rating">[^\d]+([^<]+)<.*?'
    patron += '<p>(.*?)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, quality, rating, scrapedplot  in matches:
        quality = " ([COLOR yellow]" + quality.strip() + "[/COLOR])"
        rating = " ([COLOR yellow]" + rating.strip() + "[/COLOR])"
        scrapedtitle = scrapedtitle.replace("&#8217;", "'").replace("&#8211;", "-")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle + quality. + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie'))

    # Extrae el paginador
    paginador = scrapertools.find_single_match(data, "<span class=\"current\">\d+</span><a href='([^']+)' class=\"inactive\">\d+</a>")
    if paginador != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_search",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=paginador,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))
				 
    return itemlist		

# ========================================================================================================================================================		

def genere(item):
    logger.info("[streamondemand-pureita vedohd] genere")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, 'Genere</a>(.*?)</ul>')
    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl=host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ========================================================================================================================================================

def year(item):
    logger.info("[streamondemand-pureita vedohd] year")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, 'Anno</a>(.*?)</ul>')
	
    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl=host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ========================================================================================================================================================

def peliculas(item):
    logger.info("[streamondemand-pureita vedohd] peliculas")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="poster">\s*<img\s*src="([^"]+)"\s*alt="([^"]+)">\s*<div class="rating">'
    patron += '<span class="icon-star2"><\/span>\s*([^<]+)<\/div>\s*<div class="mepo">\s*'
    patron += '<span class="quality">([^<]+)<\/span>\s*<\/div>\s*<a href="([^"]+)">'
    #patron += '<div class="texto">([^<]+)</div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, rating, quality, scrapedurl in matches:
        if rating:
          rating = " ([COLOR yellow]" + rating.strip() + "[/COLOR])"
        if quality:
          quality = " ([COLOR yellow]" + quality.strip() + "[/COLOR])"
        scrapedtitle = scrapedtitle.replace("&#8217;", "'").replace("&#8211;", "-")		
        scrapedplot=""	
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + quality + rating,
                 thumbnail=scrapedthumbnail,
                 url=scrapedurl,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie'))

    # Extrae el paginador
    paginador = scrapertools.find_single_match(data, '<a class=\'arrow_pag\' href="([^"]+)"><i id=\'nextpagination\' class=\'icon-caret-right\'>')
    if paginador != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=paginador,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ========================================================================================================================================================

def peliculas_imdb(item):
    logger.info("[streamondemand-pureita vedohd] peliculas_imdb")
    itemlist = []
    minpage = 10

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)
		
    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<img\s*src="([^"]+)" \/><\/a><\/div><\/div>\s*<div class="puesto">(.*?)<\/div>\s*'
    patron += '<div class="rating">(.*?)<\/div>\s*<div class="title"><a href="([^"]+)">([^<]+)<\/a>'

    matches = re.compile(patron, re.DOTALL).findall(data)


    for i, (scrapedthumbnail, position, rating, scrapedurl, scrapedtitle) in enumerate(matches):
        if (p - 1) * minpage > i: continue
        if i >= p * minpage: break
        position = "[COLOR red]" + position.strip() + "[/COLOR] - "
        rating = " ([COLOR yellow]" + rating.strip() + "[/COLOR])"
        scrapedtitle = scrapedtitle.replace("&#8217;", "'").replace("&#8211;", "-")
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=position + "[COLOR azure]" + scrapedtitle + "[/COLOR]" + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))

    # Extrae el paginador
    if len(matches) >= p * minpage:
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

# ========================================================================================================================================================

def findvideos(item):
    logger.info("[streamondemand-pureita vedohd] findvideos")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
	
    # Extrae las entradas (carpetas)
    patron = '<a class="options" href="#option-(\d+)">\s*<b class="icon-play_arrow"></b>\s*(.*?)\s*</a></li>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for option, scrapedtitle  in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title="[[COLOR orange]" + scrapedtitle + "[/COLOR]] " + item.title,
                 fulltitle=item.title,
                 show=item.show,
                 url=item.url,
                 thumbnail=item.thumbnail,
                 extra=option,
                 plot=item.plot,
                 folder=True))

    return itemlist

# ========================================================================================================================================================

def play(item):
    logger.info("[streamondemand-pureita vedohd] play")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)
          
    patron = ('<div id="option-%s" class="play-box-iframe fixidtab">\s*<iframe class="metaframe rptss" src="([^"]+)" [^>]+></iframe>' % item.extra)
    matches = re.compile(patron, re.DOTALL).findall(data)
	
    for scrapedurl in matches:
        data = scrapertools.anti_cloudflare(scrapedurl.strip(), headers)
        videos = servertools.find_video_items(data=data)
        for video in videos:
            itemlist.append(video)
			
    for videoitem in itemlist:
        servername = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "[[COLOR orange]" + servername.capitalize() + "[/COLOR]] " + item.fulltitle
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
    return itemlist

# ========================================================================================================================================================