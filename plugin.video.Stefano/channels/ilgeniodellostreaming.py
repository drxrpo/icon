# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canal para ilgeniodellostreaming
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

__channel__ = "ilgeniodellostreaming"
host = "http://ilgeniodellostreaming.org"
headers = [['Referer', host]]

# ==================================================================================================================================================

def mainlist(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita[/COLOR]",
                     action="peliculas",
                     url="%s/film/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Archivio A-Z[/COLOR]",
                     action="peliculas_az",
                     url="%s/film-a-z/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Archivio[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serie/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Aggiornate[/COLOR]",
                     action="peliculas_tvnew",
                     url="%s/aggiornamenti-serie/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - TV Show[/COLOR]",
                     action="peliculas_tv",
                     url="%s/tv-show/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Anime[COLOR orange] - Novita[/COLOR]",
                     action="peliculas_tv",
                     url="%s/anime/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==================================================================================================================================================

def categorias(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h2>Genere</h2>(.*?)</ul></div>')

    # Extrae las entradas (carpetas)
    patron = '<li class[^>]+><a href="([^"]+)" >([^<]+)</a></li>'
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
    logger.info("[streamondemand-pureita ilgeniodellostreaming] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto

    try:
        return peliculas_search(item)

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)

    return []

# ==================================================================================================================================================

def peliculas_search(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] peliculas_search")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)"><img src="([^"]+)"\s*alt="([^"]+)".*?>'
    patron += '<span class[^>]+>([^<]+)<\/span>.*?'
    patron += '<span class="rating">(.*?)<\/span>' 	
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, genre, rating in matches:
        scrapedplot = ""
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        rating = "  [[COLOR yellow]" + rating + "[/COLOR]]"
        rating = rating.replace("  [[COLOR yellow]" + "" + "[/COLOR]]", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if not "TV" in genre else "episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie' if not "TV" in genre else "tv" ))

    return itemlist

# ==================================================================================================================================================
	
def peliculas(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<article id="[^"]+" class="([^"]+)"><div class="poster">\s*<a href="([^"]+)">'
    patron += '<img src="([^"]+)"\s*alt="([^"]+)"></a>.*?<div class="texto">(.*?)<div class="degradado">' 
    matches = re.compile(patron, re.DOTALL).findall(data)

    for genre, scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        scrapedtitle = scrapedtitle.replace("&#8217;", "")
        scrapedtitle = scrapedtitle.replace("#038;", " ")
        scrapedtitle = scrapedtitle.replace(":", " - ")
        scrapedtitle = scrapedtitle.replace("&", " e")
        scrapedtitle = scrapedtitle.replace("e#8211;", " - ")
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if not "tvshows" in genre else "episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie' if not "tvshows" in genre else "tv" ))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="icon-chevron-right">'
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

# ==================================================================================================================================================
	
def peliculas_az(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] peliculas_az")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)" /><\/a></td><td class="mlnh-2">'
    patron += '<a href="(.*?)">(.*?)</a></td><td>(.*?)</td>.*?'
    patron += '<span class="labelimdb">(.*?)</span>'	
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle, year, rating, in matches:
        scrapedplot = ""
        rating = " [[COLOR yellow]" + rating + "[/COLOR]]"
        rating = rating.replace(" [[COLOR yellow]" + "" + "[/COLOR]]", "")
        year = " [[COLOR yellow]" + year + "[/COLOR]]"
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR] " + year + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="icon-chevron-right">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_az",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def peliculas_tv(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] peliculas_tv")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<div class="poster">\s*<a href="(.*?)">'
    patron += '<img\s*src="(.*?)"\s*alt="(.*?)"></a>.*?'
    patron += '<div class="texto">(.*?)<div class[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="icon-chevron-right">'
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

# ==================================================================================================================================================
	
def peliculas_tvnew(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] peliculas_tvnew")
    itemlist = []
    PERPAGE = 14
	
    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)" alt="[^"]+"><div class[^>]+><a href="([^"]+)">'
    patron += '<span class[^>]+>.*?</span><span class="a">.*?'
    patron += '</span><span class[^>]+>([^<]+)</span>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedthumbnail, scrapedurl, scrapedtitle) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedplot = ""
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios_new",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_tvnew",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def episodios(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] episodios")
    itemlist = []


    patron='<ul class="episodios">(.*?)</ul>'

    data = httptools.downloadpage(item.url, headers=headers).data
    matches = re.compile(patron, re.DOTALL).findall(data)

    for match in matches:
        patron = '<img src="(.*?)"><\/a><\/div><div\s*class="numerando">(.*?)'
        patron += '<\/div><div class[^>]+><a href="(.*?)">(.*?)<\/a>'
        episodi = re.compile(patron, re.DOTALL).findall(match)

        for scrapedthumbnail, scrapedep, scrapedurl, scrapedtitle in episodi:
            scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title= "[COLOR azure]" + scrapedep + "  [COLOR orange]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=item.plot,
                     folder=True))
								 


    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title=item.title + " [COLOR yellow] Aggiungi alla libreria [/COLOR]",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))
        itemlist.append(
            Item(channel=item.channel,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios",
                 show=item.show))

    return itemlist

# ==================================================================================================================================================

def episodios_new(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '</script></div><div class="sbox"><h2>(.*?)</div></div><script>')

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)"><\/a><\/div><div\s*class="numerando">([^<]+)<\/div>'
    patron += '<div class[^>]+><a\s*href="([^"]+)">([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapededthumbnail, scrapedep, scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedep + " " + scrapedtitle,
                 show=scrapedep + " " + scrapedtitle,
                 title="[COLOR azure]" +scrapedep + "  [COLOR orange]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))
				 
    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title=item.title + " [COLOR yellow] Aggiungi alla libreria [/COLOR]",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))
        itemlist.append(
            Item(channel=item.channel,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios",
                 show=item.show))

    return itemlist

# ==================================================================================================================================================
	
def findvideos(item):
    logger.info("[streamondemand-pureita ilgeniodellostreaming] findvideos")

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<td><a class="link_a" href="(.*?)" target="_blank">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for url in matches:
        html = scrapertools.cache_page(url, headers=headers)
        data += str(scrapertools.find_multiple_matches(html, 'window.location.href=\'(.*?)\''))

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + " [COLOR orange]" + videoitem.title + "[/COLOR]"
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

