# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale SerieTVU
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# By MrTruth
# ------------------------------------------------------------

import re

from core import logger
from core import httptools
from core import config
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "serietvu"
host = "https://www.serietvu.club/"

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'],
           ['Accept-Encoding', 'gzip, deflate'],
           ['Referer', host]]

def isGeneric():
    return True

def mainlist(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] mainlist")
    itemlist = [Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Serie TV[COLOR orange][B] - Nuove[/COLOR][/B]",
                     url="%s/category/serie-tv" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     action="tvserie_new",
                     title="[COLOR azure]Serie TV[COLOR orange][B] - Aggiornate[/COLOR][/B]",
                     url="%s/ultimi-episodi" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     action="latestep",
                     title="[COLOR azure]Serie TV[COLOR orange][B] - Ultimi Episodi[/COLOR][/B]",
                     url="%s/ultimi-episodi" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Serie TV[COLOR orange][B] - TV Show[/COLOR][/B]",
                     url="%s/category/tv-show/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Serie TV[COLOR orange][B] - Categorie[/COLOR][/B]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================
	
def search(item, texto):
    logger.info("[StreamOnDemand-PureITA SerieTVU] search")
    item.url = host + "/?s=" + texto
    try:
        return lista_serie(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================
		
def categorie(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] categorie")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)
    blocco = scrapertools.get_match(data, 'Calendario Aggiornamenti</a></li>(.*?)</ul>\s*</section>')
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
	if "Tv Show" in scrapedtitle:  continue
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_serie",
                 title=scrapedtitle,
                 contentType="tv",
                 url="%s%s" % (host, scrapedurl),
                 thumbnail=item.thumbnail,
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def latestep(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] latestep")
    itemlist = []
    PERPAGE = 21

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)
		
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = r'<div class="item">\s*<a href="([^"]+)" data-original="([^"]+)" class="lazy inner">'
    patron += r'[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)<small>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedurl, scrapedimg, scrapedtitle, scrapedinfo) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        episodio = re.compile(r'(\d+)x(\d+)', re.DOTALL).findall(scrapedinfo)
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos_ep",
                 title="%s %s" % ("[B]" + scrapedtitle + "[/B]", scrapedinfo),
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra=episodio,
                 thumbnail=scrapedimg,
                 show=title,
                 folder=True), tipo="tv"))
				 
    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="latestep",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def tvserie_new(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] latestep")
    itemlist = []
    PERPAGE = 21

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina

    data = httptools.downloadpage(item.url).data

    # Estrae i contenuti 
    patron = '<div class="item">\s*<a href="([^"]+)" data-original="([^"]+)" class="lazy inner">'
    patron += '[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)<small>[^<]+<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for i, (scrapedurl, scrapedimg, scrapedtitle ) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedimg,
                 show=scrapedtitle,
                 folder=True), tipo='tv'))
				 
    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="tvserie_new",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
	
# ==============================================================================================================================================================================
	
def lista_serie(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] lista_serie")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)

    patron = '<div class="item">\s*<a href="([^"]+)" data-original="([^"]+)" class="lazy inner">\s*'
    patron += '<span class="brand"></span>\s*<div>\s*<div class="title">([^"]+)<br><div class="stars" title="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedimg, scrapedtitle, voto in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle + " ([COLOR yellow]" + voto + "[/COLOR])",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedimg,
                 show=scrapedtitle,
                 folder=True), tipo="tv"))

    # Pagine
    patron = r'<li><a href="([^"]+)" >Pagina successiva &raquo;</a></li>'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page:
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_serie",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))
	 
    return itemlist

# ==============================================================================================================================================================================
	
def episodios(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = r'<option value="(\d+)"[\sselected]*>.*?</option>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for value in matches:
        patron = r'<div class="list [active]*" data-id="%s">(.*?)</div>\s*</div>' % value
        blocco = scrapertools.find_single_match(data, patron)

        patron = r'(<a data-id="\d+[^"]*" data-href="([^"]+)" data-original="([^"]+)" class="[^"]+">)[^>]+>[^>]+>([^<]+)<'
        matches = re.compile(patron, re.DOTALL).findall(blocco)
        for scrapedextra, scrapedurl, scrapedimg, scrapedtitle in matches:
            number = scrapertools.decodeHtmlentities(scrapedtitle.replace("Episodio", "")).strip()
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     title=item.show + " - [B]" + value + "x" + number.zfill(2) + "[/B]",
                     fulltitle=scrapedtitle,
                     contentType="episode",
                     url=scrapedurl,
                     thumbnail=scrapedimg,
                     extra=scrapedextra,
                     plot=item.plot,
                     folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def findvideos(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] findvideos")
    itemlist = servertools.find_video_items(data=item.extra)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.channel = __channel__
        videoitem.title =  "".join([item.title, ' [[COLOR orange][B]' + server + '[/B][/COLOR]]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.show = item.show

    return itemlist

# ==============================================================================================================================================================================

def findvideos_ep(item):
    logger.info("[StreamOnDemand-PureITA SerieTVU] findvideos_ep")

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = r'<div\s*class="list [active]*"\s*data-id="%s">(.*?)<a\s*class="back" title="Chiudi"></a>' % item.extra[0][0]
    blocco = scrapertools.find_single_match(data, patron)

    patron = r'<a\s*data-id="%s[^"]*"\s*data-href="([^"]+)"\s*data-original="([^"]+)"\s*class="[^"]+">' % item.extra[0][1].lstrip("0")
    matches = re.compile(patron, re.DOTALL).findall(blocco)
    itemlist = servertools.find_video_items(data=matches[0][0])

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.channel = __channel__
        videoitem.title =  "".join([item.title, ' [[COLOR orange][B]' + server + '[/B][/COLOR]]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.show = item.show

    return itemlist



