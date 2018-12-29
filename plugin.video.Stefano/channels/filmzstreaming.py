# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  FilmZStreaming
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger 
from core import httptools
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmzstreaming"
host = "https://filmzstreaming.pw/"

headers = [['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'],
           ['Accept-Encoding', 'gzip, deflate'],
           ['Referer', host]]


def mainlist(item):
    logger.info("streamondemand-pureita.FilmZStreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Cinema'[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita[/COLOR]",
                     action="peliculas_new",
                     url="%s/film/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categoria[/COLOR]",
                     action="genres",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Anno[/COLOR]",
                     action="years",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Novita[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serietv/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
               Item(channel=__channel__,
                     title="[COLOR orange]Cerca ...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ========================================================================================================================================================

def genres(item):
    logger.info("[streamondemand-pureita.FilmZStreaming] genres")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, "Categorie FILM</a>(.*?)DMCA</a>")

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_new" if not "SERIE" in scrapedtitle else "peliculas_tv",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist
	
# ========================================================================================================================================================

def years(item):
    logger.info("[streamondemand-pureita.FilmZStreaming] years")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, "<h2>Film Per Anno</h2>(.*?)</ul></nav>")

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_new",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

	
# ========================================================================================================================================================
		
def peliculas(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)" alt="([^"]+)"><div class="rating"><span class[^>]+>'
    patron += '</span>\s*([^<]+)</div><div class="featu">[^>]+><a href="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url, match.group(4))
        rating = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedthumbnail = scrapertools.unescape(match.group(1))
        scrapedtitle = scrapedtitle.replace("&#8217;", "'").replace("&#8211;", "-").replace("’", "'")
        scrapedtitle = scrapedtitle.replace("Streaming", "").replace("Online", "")
        scrapedtitle = scrapedtitle.replace("[", "(").replace("]", ")")
        rating = " ([COLOR yellow]" + rating + "[/COLOR])"
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador				 
    patronvideos = "<span class=\"current\">\d+</span><a href='([^']+)' class=\"inactive\">\d+</a>"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
	
# ========================================================================================================================================================

def peliculas_new(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas_new")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)"\s*alt="([^"]+)"><div class="rating">[^>]+><\/span>\s*([^<]+)<\/div>'
    patron += '<div class="mepo">\s*<span class="quality">([^<]+)<\/span><\/div>\s*'
    patron += '<a href="([^"]+)">.*?<div class="texto">(.*?)<'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:

        scrapedplot = scrapertools.unescape(match.group(6))
        scrapedurl = urlparse.urljoin(item.url, match.group(5))
        quality = scrapertools.unescape(match.group(4))
        rating = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedthumbnail = scrapertools.unescape(match.group(1))
		
        scrapedtitle = scrapedtitle.replace("&#8217;", "'").replace("&#8211;", "-").replace("’", "'")
        scrapedtitle = scrapedtitle.replace("Streaming", "").replace("Online", "")
        scrapedtitle = scrapedtitle.replace("[", "(").replace("]", ")").replace(" HD", "")
		
        quality = quality.replace("FullHD", "Full-HD").replace("1080p", "")
        quality = quality.replace("HDCAM", "HD-CAM").replace("720p", "")
        if rating == "0":
          rating = ""
        else:
          rating = " ([COLOR yellow]" + rating + "[/COLOR])"
        quality = " ([COLOR yellow]" + quality + "[/COLOR])"
		
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + quality + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = "<span class=\"current\">\d+</span><a href='([^']+)' class=\"inactive\">\d+</a>"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_new",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ========================================================================================================================================================	
		
def peliculas_tv(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas_tv")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)"\s*alt="([^"]+)"><div class="rating">[^>]+>'
    patron += '<\/span>\s*([^<]+)<\/div><div class="mepo">\s*<\/div>\s*'
    patron += '<a\s*href="([^"]+)">.*?<div class="texto">(.*?)<'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:

        scrapedplot = scrapertools.unescape(match.group(5))
        scrapedurl = urlparse.urljoin(item.url, match.group(4))
        rating = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedthumbnail = scrapertools.unescape(match.group(1))
        #scrapedtitle = scrapedtitle.title()
        scrapedtitle = scrapedtitle.replace("&#8217;", "'").replace("&#8211;", "-").replace("’", "'")
        scrapedtitle = scrapedtitle.replace("!", "").replace("Online", "").replace(" ITA ", " ")
        scrapedtitle = scrapedtitle.replace("[", "(").replace("]", ")").replace(" HD", "").replace("SerieTv", "")
        scrapedtitle = scrapedtitle.replace("SerieTV", "").replace("Serie-Tv", "").replace("ONLINE", "")
        scrapedtitle = scrapedtitle.replace("STREAMING", "").replace("streaming", "").replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("serie", "").replace("Serie TV", "").replace("Serie-TV", "")
        if rating == "0":
          rating = ""
        else:
          rating = " ([COLOR yellow]" + rating + "[/COLOR])"
		
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 contentType="serie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = "<span class=\"current\">\d+</span><a href='([^']+)' class=\"inactive\">\d+</a>"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ========================================================================================================================================================

def episodios(item):
    logger.info("streamondemand-pureita.FilmZStreaming episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<img src="([^"]+)"></a></div><div class="numerando">([^<]+)</div>'
    patron += '<div class="episodiotitle">\s*<a href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedep, scrapedurl, scrapedtitle  in matches:
        scrapedep= scrapedep.replace(" - ", "x")
        scrapedep= "([COLOR orange]" + scrapedep + "[/COLOR]) "
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedep + "[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 contentType="episode",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot="[COLOR orange]" + item.fulltitle + "[/COLOR]  " + item.plot,
                 folder=True))

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))
        itemlist.append(
            Item(channel=__channel__,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios",
                 show=item.show))

    return itemlist

# ========================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita.FilmZStreaming ] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        if item.extra == "movie":
            return peliculas_search(item)
        if item.extra == "serie":
            return peliculas_search(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ========================================================================================================================================================
		
def peliculas_search(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas_search")
    itemlist = []
 
    data = httptools.downloadpage(item.url).data

    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)" alt="(.*?)" />\s*<span class="(.*?)">.*?'
    patron += '<span class="rating">[^\d]+([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, genre, rating in matches:
        scrapedtitle = scrapedtitle.replace("&#8217;", "'").replace("&#8211;", "-").replace("’", "'")
        scrapedtitle = scrapedtitle.replace("serie", "").replace("Online", "").replace(" ITA ", " ")
        scrapedtitle = scrapedtitle.replace("[", "(").replace("]", ")").replace(" HD", "").replace("SerieTv", "")
        scrapedtitle = scrapedtitle.replace("SerieTV", "").replace("Serie-Tv", "").replace("ONLINE", "")
        scrapedtitle = scrapedtitle.replace("STREAMING", "").replace("streaming", "").replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("!", "").replace("Serie TV", "").replace("Serie-TV", "")
        if rating == "0":
          rating = ""
        else:
          rating = " ([COLOR yellow]" + rating + "[/COLOR])"
        if "tvshows" in genre:
           genres = " ([COLOR yellow]Serie TV[/COLOR])"
        else:
           genres =""
        scrapedplot = ""
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios" if not "movies" in genre else "findvideos",
                 contentType="movie",
                 title=title + genres + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='tv' if not "movies" in genre else 'movie'))

    return itemlist
	
# ========================================================================================================================================================		

def findvideos(item):

    data = scrapertools.anti_cloudflare(item.url, headers)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR orange]' + videoitem.title + '[/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
