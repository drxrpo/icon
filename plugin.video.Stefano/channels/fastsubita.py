# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  fastsubita
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse
import xbmc

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "fastsubita"
host = "http://fastsubita.gq/"
headers = [['Referer', host]]



def mainlist(item):
    logger.info("[streamondemand-pureita fastsubita] mainlist")
    itemlist = [#Item(channel=__channel__,
                     #title="[COLOR azure]Serie TV [COLOR orange] - In Evidenza[/COLOR]",
                     #action="peliculas_home",
                     #extra="serie",
                     #url=host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Ultimi Episodi[/COLOR]",
                     action="peliculas_episodios",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV [COLOR orange] - Elenco[/COLOR]",
                     action="peliculas_tv",
                     extra="serie",
                     url="%s/tutte-le-serie-tv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita.fastsubita] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        return peliculas_episodios(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
	
# ==================================================================================================================================================	

def peliculas_home(item):
    logger.info("streamondemand-pureita.fastsubita peliculas_home")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">\s*<div class="slide-title">([^-]+)([^<]+)</div>\s*</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedep in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle = scrapedtitle.title()
        scrapedep = scrapedep.lower()
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="peliculas_episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[COLOR orange]" + scrapedep + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))
			 

    return itemlist
	
# ==================================================================================================================================================
"""
def peliculas_update(item):
    logger.info("[streamondemand-pureita.fastsubita] peliculas_update")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)" title="([^\d+]+)([^<]+)"><img width[^s]+src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedep, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        scrapedtitle = scrapedtitle.lower()
        scrapedtitle = scrapedtitle.capitalize()

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[COLOR orange] " + scrapedep + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = 'href="([^"]+)">Successivi</a></div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])

        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_update",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 extra=item.extra,
                 folder=True))

    return itemlist
"""	
# ==================================================================================================================================================

def peliculas_tv(item):
    logger.info("[streamondemand-pureita.fastsubita] peliculas_tv")
    itemlist = []
    PERPAGE = 14
	
    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<li class="cat-item cat-item-\d+"><a href="(.*?\/\/[^\/]+\/[^\/]+\/([^\/]+)[^"]+)" >([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedurl, scrapetitle, scrapedtitle ) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapetitle = scrapetitle.replace("-percento", "%") 
        scrapetitle = scrapetitle.replace("-", " ").capitalize()
        if not "http:" in scrapedurl:
          scrapedurl = "http:" + scrapedurl
        if "Stagione" in scrapedtitle:
          scrapedtitle = scrapetitle + "  ([COLOR orange]" + scrapedtitle + "[/COLOR])"
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="peliculas_episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))
				 
    return itemlist

# ==================================================================================================================================================
"""
def episodios_elenco(item):
    logger.info("[streamondemand-pureita.fastsubita] episodios_elenco")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)" title[^>]+><img width[^>]+src="([^"]+)"[^>]+alt="([^(]+)([^<]+)"\s*\/>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedep in matches:
        scrapedplot = ""
        scrapedtitle = scrapedtitle.lower()
        scrapedtitle = scrapedtitle.capitalize()
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[COLOR orange]" + scrapedep + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 extra=item.extra,
                 folder=True), tipo='tv'))


    return itemlist
	
"""	
# ==================================================================================================================================================

def peliculas_episodios(item):
    logger.info("[streamondemand-pureita.fastsubita] peliculas_episodios")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    # Extrae las entradas (carpetas)
    patron = '<h3 class=".*?title-font"><a href="([^"]+)" rel="bookmark">(.*?[^\s]+[^\d+]+)([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedep in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapedtitle.title()
        scrapedtitle = scrapedtitle.replace("’", "'")
        scrapedtitle = scrapedtitle.replace("&#", "")
        scrapedep = scrapedep.replace("8211;", "").replace("8217;", "")
        scrapedep = scrapedep.replace("&#8220;", "").replace("&#8221;", "")

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if "serie" in item.extra else "findvideos_tv",
                 contentSerieName=scrapedtitle,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[COLOR orange] " + scrapedep + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = 'href="([^"]+)">Successivi</a></div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])

        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_episodios",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 extra=item.extra,
                 folder=True))

    return itemlist

# ==============================================================================================================================================


def findvideos_tv(item):
    logger.info("[streamondemand-pureita.fast] findvideos_tv")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<h2>Streaming(.*?)<footer class="entry-footer">')
    patron = r'<a href="([^"]+)">([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if "http" in scrapedtitle or "Seriespedia" in scrapedtitle:
          continue
       
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title="[[COLOR yellow]" + scrapedtitle + "[COLOR]] " + item.title,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))
				 
    patron = r'<a href="([^"]+)">http[^\/]+\/\/([^\/]+).*?<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("www.", "").replace(".me", "")
        scrapedtitle = scrapedtitle.replace(".co", "").replace(".net", "")
        scrapedtitle = scrapedtitle.replace(".li", "").replace(".tv", "")
        scrapedtitle = scrapedtitle.capitalize()
        if "Seriespedia" in scrapedtitle:
          continue
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title="[[COLOR yellow]" + scrapedtitle + "[/COLOR]] " + item.title,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))
    return itemlist



def play(item):
    logger.info("[streamondemand-pureita.fastsubita] play")
    data = httptools.downloadpage(item.url).data
    
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join([item.title, '[COLOR orange][B]' + ' ' + server + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
    return itemlist

