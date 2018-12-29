# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita / XBMC Plugin
# Canal para piratestreaming
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

__channel__ = "piratestreaming"

host = "http://www.piratestreaming.club"
DEBUG = config.get_setting("debug")

def mainlist(item):
    logger.info()
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/category/films/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Aggiornati HD[/COLOR]",
                     action="peliculas_hd",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV - [COLOR orange]Novita'[/COLOR]",
                     extra="serie",
                     action="peliculas_tv",
                     url="%s/category/serie/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV - [COLOR orange]Ultimi Episodi[/COLOR]",
                     extra="serie",
                     action="peliculas_lasttv",
                     url="%s/category/serie/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Anime - [COLOR orange]Archivio[/COLOR]",
                     extra="serie",
                     action="peliculas_tv",
                     url="%s/category/anime-cartoni-animati/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ========================================================================================================================================================

def peliculas(item):
    logger.info()
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = r'<a\s*data-toggle="tooltip" data-placement="bottom" title="([^"]+)" alt=".*?\s*'
    patron += 'href="([^"]+)">\s*<img\s*class="img-responsive " title="[^"]+" alt="[^"]+" src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        scrapedtitle = scrapedtitle.replace("&", "e")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        item = infoSod(
                Item(channel=__channel__,
                    action="findvideos",
                    contentType="movie",
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    plot="",
                    folder=True), tipo='movie')
        if not item.plot:
            try:
                daa = httptools.downloadpage(scrapedurl).data
                patron = '<div\s*class="col-xs-9">([^<]+)</div>'
                item.plot = scrapertools.decodeHtmlentities(scrapertools.find_single_match(daa, patron)).strip()
            except:
                item.plot = "Trama non disponibile"
        itemlist.append(item)

    # Extrae el paginador
    patronvideos = '<a\s*class="nextpostslink" rel="next" href="([^"]+)">Avanti'
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

def peliculas_hd(item):
    logger.info()
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = r'<a\s*data-toggle="tooltip" data-placement="bottom" title="([^"]+)"\s*'
    patron += 'style[^>]+href="([^"]+)">\s*<img\s*[^>]+src="([^"]+)"\s*[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        scrapedtitle = scrapedtitle.replace("&", "e")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        item = infoSod(
                Item(channel=__channel__,
                    action="findvideos",
                    contentType="movie",
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    plot="",
                    folder=True), tipo='movie')
        if not item.plot:
            try:
                daa = httptools.downloadpage(scrapedurl).data
                patron = '<div\s*class="col-xs-9">([^<]+)</div>'
                item.plot = scrapertools.decodeHtmlentities(scrapertools.find_single_match(daa, patron)).strip()
            except:
                item.plot = "Trama non disponibile"
        itemlist.append(item)


    return itemlist

# ========================================================================================================================================================
	
def peliculas_tv(item):
    logger.info()
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = r'<a\s*data-toggle="[^"]+" data-placement="[^"]+" title="([^"]+)"[^h]+'
    patron += r'href="([^"]+)">\s*<img[^t]+title="[^"]+" alt="[^"]+" src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        item = infoSod(
                Item(channel=__channel__,
                    action="episodios",
                    contentType="tv",
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    plot="",
                    folder=True), tipo='tv')
        if not item.plot:
            try:
                daa = httptools.downloadpage(scrapedurl).data
                patron = '<div\s*class="col-xs-9">([^<]+)</div>'
                item.plot = scrapertools.decodeHtmlentities(scrapertools.find_single_match(daa, patron)).strip()
            except:
                item.plot = "Trama non disponibile"
        itemlist.append(item)

    # Extrae el paginador
    patronvideos = '<a\s*class="nextpostslink" rel="next" href="([^"]+)">Avanti'
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

def peliculas_lasttv(item):
    logger.info()
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = r'<a\s*rel="nofollow" title="[^"]+" alt="[^"]+" href="([^"]+)">'
    patron += r'[^>]+>[^>]+>[^>]+>\s*([^<]+)<\/div>.*?<small>\s*([^<]+)\s*</small><'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, ep in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        ep=ep.replace("(", "").replace(")", "").strip()
        ep=" ([COLOR orange]" + ep + "[/COLOR])"
        scrapedthumbnail=""
        item = infoSod(
                Item(channel=__channel__,
                    action="episodios",
                    contentType="tv",
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + ep,
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    plot="",
                    folder=True), tipo='tv')
        if not item.plot:
            try:
                daa = httptools.downloadpage(scrapedurl).data
                patron = '<div\s*class="col-xs-9">([^<]+)</div>'
                item.plot = scrapertools.decodeHtmlentities(scrapertools.find_single_match(daa, patron)).strip()
            except:
                item.plot = "Trama non disponibile"
        itemlist.append(item)


    return itemlist

# ========================================================================================================================================================

def search(item, texto):
    logger.info()

    item.url = host + "/?s=" + texto

    try:
        return cerca(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ========================================================================================================================================================

def cerca(item):
    itemlist = []
    itype = ''

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = r'<a\s*data-toggle="[^"]+" data-placement="[^"]+" title="([^"]+)" alt="[^"]+"'
    patron += r' href="([^"]+)">\s*<img[^t]+title="([^"]+)" alt="[^"]+" src="([^"]+)"[^>]+>'
    matches = re.compile(patron).findall(data)

    for scrapedtitle, scrapedurl, scrapedtitleextra, scrapedthumbnail in matches:
        if 'serie' in scrapedtitleextra: 
            itype = 'serie'
            scrapedtitle += " ([COLOR red]Serie TV[/COLOR])"
        elif 'film' in scrapedtitleextra:
            itype = 'film'
            scrapedtitle += " ([COLOR red]Film[/COLOR])"
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if itype == "serie" else "findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie' if itype == 'film' else 'tv'))

    # Extrae el paginador
    patronvideos = '<a\s*class="nextpostslink" rel="next" href="([^"]+)">Avanti'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="cerca",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ========================================================================================================================================================

def episodios(item):
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = r'<span\s*class="prev-link-episode">(.*?)<\/span>\s*<a[^h]+href="[^=]+="([^"]+)".*?>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        # Fix Titolo ----------------------------------------------------------------
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = re.sub("\s+", " ", scrapedtitle).replace("-", " ").strip()
        n = scrapertools.find_single_match(scrapedtitle, '(\d+x\d+)')
        scrapedtitle = re.sub(n, n + " -", scrapedtitle)
        # ============================================================================

        itemlist.append( 
            Item(channel=__channel__, 
                 action="findvid_serie",
                 contentType="episode", 
                 title=scrapedtitle, 
                 url=scrapedurl, 
                 thumbnail=item.thumbnail, 
                 extra=data, 
                 fulltitle=scrapedtitle,
                 plot="[COLOR orange]" + item.fulltitle + "[/COLOR] " + item.plot,				 
                 show=item.show))


    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))

    return itemlist

# ========================================================================================================================================================

def findvid_serie(item):
    logger.info()

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.title = "".join(['[COLOR azure][[COLOR orange]' + server + '[/COLOR]] - ' + item.fulltitle + '[/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot=item.plot
        videoitem.channel = __channel__

    return itemlist

# ========================================================================================================================================================
	
def findvideos(item):
    logger.info("[streamondemand-pureita piratestreaming] findvideos")

    data = httptools.downloadpage(item.url).data
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.title = "".join(['[COLOR azure][[COLOR orange]' + server + '[/COLOR]] - ' + item.fulltitle + '[/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot=item.plot
        videoitem.channel = __channel__
    return itemlist