# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# PureITA - XBMC Plugin
# Canale  filmhdfull
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger, httptools
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmhdfull"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "filmhdfull (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.ffhd.pw"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host],
    ['Cache-Control', 'max-age=0']
]

def isGeneric():
    return True


def mainlist(item):
    logger.info("pureita.filmhdfull mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Ultime Novita'[/COLOR]",
                     action="peliculas",
                     url=host+"/movies/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Top IMDB[/COLOR]",
                     action="peliculas",
                     url="%s/top-imdb/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Per Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Per Paese[/COLOR]",
                     action="country",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Cerca [COLOR yellow]Film...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),					 
                 Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     action="serie",
                     url=host+"/series",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Cerca [COLOR yellow]Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================


def categorias(item):
    logger.info("pureita.filmhdfull categorias")
    itemlist = []
    
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, "<ul class='sub-menu'>(.*?)</ul>")

    
    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================	
	
	
def country(item):
    logger.info("pureita.filmhdfull categorias")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, "<a>Paesi</a>(.*?)</ul>")

    
    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png",
                 folder=True))

    return itemlist	

# ==============================================================================================================================================	
	
def search(item, texto):
    logger.info("[filmhdfull.py] " + item.url + " search " + texto)

    try:

        if item.extra == "movie":
            item.url = host +"/?s=" + texto
            return movie_src(item)
        if item.extra == "serie":
            item.url = host +"/?s=" + texto
            return serie(item)

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# ==============================================================================================================================================	
	
def peliculas_src(item):
    logger.info("pureita.filmhdfull peliculas")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<div class="thumbnail animation-2">\s*<a href="(.*?)">\s*<img src="(.*?)" alt="(.*?)"/>\s*[^>]+>\s*(.*?) </span>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedtipo in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")

        if scrapedtipo=="TV":
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="serie",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     folder=True), tipo='tv'))
        else:
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="findvideos",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     folder=True), tipo='movie'))

    return itemlist

# ==============================================================================================================================================	


def movie_src(item):
    logger.info("[ffHD.py]==> film")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    start = data.find('<div class="movies-list movies-list-full">')
    data = data[start:]
    patron = r'<a href="([^"]+)"[^>]+>[^>]+>[^>]+>[^<]+<img data-original="([^"]+)"[^>]+>[^>]+><h2>([^<]+)</h2>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedimg, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        if "/adult/" not in scrapedurl:
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="findvideos",
                     title=scrapedtitle,
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     thumbnail=scrapedimg.strip(),
                     extra=item.extra,
                     folder=True), tipo="movie"))


    patron = r"<li class=[\"']active[\"']><a[^>]*?>\d+</a></li><li><a.+?href=[\"']([^\"']+)[\"']>"
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title=color("Torna Home", "yellow"),
                 folder=True))
        itemlist.append(
            Item(channel=__channel__,
                 action="movie_src",
                 title=color("Successivo >>", "yellow"),
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist
# ==============================================================================================================================================
	
def peliculas(item):
    logger.info("pureita.filmhdfull peliculas")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)

    
    patron = '<a href="([^"]+)" data-url="" class="ml-mask jt" data-hasqtip="112" oldtitle=".*?" title="">\s*'
    patron += '<span class="mli-quality">.*?<\/span>.*?\s*<img data-original="([^"]+)" class="lazy thumb mli-thumb" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
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

    
    patronvideos = r"<li class='active'><a class=''>.*?</a></li><li><a rel='nofollow' class='page larger' href='(.*?)'"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================	
	
def serie(item):
    logger.info("pureita.filmhdfull peliculas")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)

    
    patron = '<a href="([^"]+)" data-url="" class="ml-mask jt" data-hasqtip="112" oldtitle=".*?" title="">\s*'
    patron += '<img data-original="([^"]+)" class="lazy thumb mli-thumb" alt=".*?">\s*<span class="mli-info"><h2>(.*?)</h2>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="puntate",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

   
    patronvideos = r"<li class='active'><a class=''>.*?</a></li><li><a rel='nofollow' class='page larger' href='(.*?)'"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================
	
def puntate(item):
    logger.info("pureita.filmhdfull categorias")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, '<div class="les-content" style="display: block">([^+]+)</ul>')

    
    patron = '<a href="([^"]+)">([^"]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png",
                 folder=True))

    return itemlist	
	
# ==============================================================================================================================================

def findvideos(item):
    logger.info("[filmhdfull.py] play")

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<td><a class="link_a" href="(.*?)" target="_blank">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for url in matches:
        html = scrapertools.cache_page(url, headers=headers)
        data += str(scrapertools.find_multiple_matches(html, 'window.location.href=\'(.*?)\''))

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist

# ==============================================================================================================================================	
	
def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")
