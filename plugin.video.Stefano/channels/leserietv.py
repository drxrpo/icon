# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureira / XBMC Plugin
# Canale LeSerieTV
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
#  By Costaplus
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

__channel__ = "leserietv"
host = 'http://www.guardareserie.tv'
headers = [['Referer', host]]

def mainlist(item):
    logger.info("streamondemand-pureita.[leserietv mainlist]")
    itemlist = [Item(channel=__channel__,
                     action="novita",
                     title="[COLOR azure]Serie TV[COLOR orange] - Novità[/COLOR]",
                     url=("%s/streaming/" % host),
                     thumbnail=thumbnail_novita,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Serie TV[COLOR orange] - Lista[/COLOR]",
                     url=("%s/streaming/" % host),
                     thumbnail=thumbnail_lista,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail=thumbnail_categoria,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="top50",
                     title="[COLOR azure]Serie TV[COLOR orange] -Top 50[/COLOR]",
                     url=("%s/top50.html" % host),
                     thumbnail=thumbnail_top,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     extra="serie",
                     action="search",
                     title="[COLOR orange]Cerca...[/COLOR]",
                     thumbnail=thumbnail_cerca,
                     fanart=FilmFanart)]
    return itemlist
# =================================================================

def novita(item):
    logger.info("streamondemand-pureita.[leserietv novità]")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<div class="video-item-cover"[^<]+<a href="(.*?)">[^<]+<img src="(.*?)" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedthumbnail = host + scrapedthumbnail
        logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle, viewmode="movie"), tipo='tv'))

    # Paginazione
    patron = '<div class="pages">(.*?)</div>'
    paginazione = scrapertools.find_single_match(data, patron)
    patron = '<span>.*?</span>.*?href="([^"]+)".*?</a>'
    matches = re.compile(patron, re.DOTALL).findall(paginazione)
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        paginaurl = matches[0]
        itemlist.append(
            Item(channel=__channel__, 
                 action="novita"  , 
                 title="[COLOR orange]Successivi>>[/COLOR]", 
                 url=paginaurl, thumbnail=thumbnail_successivo, 
                 folder=True))

    return itemlist
# =================================================================

def lista_serie(item):
    logger.info("streamondemand-pureita.[leserietv lista_serie]")
    itemlist = []

    post = "dlenewssortby=title&dledirection=asc&set_new_sort=dle_sort_cat&set_direction_sort=dle_direction_cat"
    data = httptools.downloadpage(item.url, post=post, headers=headers).data
    patron = '<div class="video-item-cover"[^<]+<a href="(.*?)">[^<]+<img src="(.*?)" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedthumbnail = host + scrapedthumbnail
        logger.info(scrapedurl + " " + scrapedtitle + scrapedthumbnail)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle, viewmode="movie"), tipo='tv'))

    # Paginazione
    patron = '<div class="pages">(.*?)</div>'
    paginazione = scrapertools.find_single_match(data, patron)
    patron = '<span>.*?</span>.*?href="([^"]+)".*?</a>'
    matches = re.compile(patron, re.DOTALL).findall(paginazione)
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        paginaurl = matches[0]
        itemlist.append(
            Item(channel=__channel__, 
			     action="novita", 
                 title="[COLOR orange]Successivi >>[/COLOR]", 
                 url=paginaurl,
                 thumbnail=thumbnail_successivo, 
                 folder=True))

    return itemlist
# =================================================================

def categorias(item):
    logger.info("streamondemand-pureita.[leserietv categorias]")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<ul class="dropdown-menu cat-menu">(.*?)</ul>')
    patron = '<li ><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_serie",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist
# =================================================================

def search(item, texto):
    logger.info("streamondemand-pureita.leserietv " + host + " search " + texto)

    itemlist = []

    post = "do=search&subaction=search&story=" + texto
    data = httptools.downloadpage(host, post=post, headers=headers).data

    patron = '<div class="video-item-cover"[^<]+<a href="(.*?)">[^<]+<img src="(.*?)" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedthumbnail = host + scrapedthumbnail
        logger.info(scrapedurl + " " + scrapedtitle + scrapedthumbnail)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv'))

    return itemlist
# =================================================================

def top50(item):
    logger.info("streamondemand-pureita.[leserietv top50]")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = 'class="top50item">\s*<[^>]+>\s*<.*?="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        scrapedthumbnail = ""
        logger.debug(scrapedurl + " " + scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle, viewmode="movie"), tipo='tv'))

    return itemlist
# =================================================================

def episodios(item):
    logger.info("streamondemand-pureita.[leserietv episodios]")
    itemlist = []
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<li id[^<]+<[^<]+<.*?class="serie-title">(.*?)</span>[^>]+>[^<]+<.*?megadrive-(.*?)".*?data-link="([^"]+)">Megadrive</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedlongtitle, scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapedtitle.split('_')[0] + "x" + scrapedtitle.split('_')[1].zfill(2)

        scrapedtitle = scrapedtitle +  scrapedlongtitle
        itemlist.append(Item(channel=__channel__,
                             action="findvideos",
                             title=scrapedtitle,
                             fulltitle=scrapedtitle,
                             url=scrapedurl,
                             thumbnail=item.thumbnail,
                             plot=item.plot,
                             fanart=item.fanart if item.fanart != "" else item.scrapedthumbnail,
                             show=item.fulltitle))


    return itemlist
# =================================================================

def findvideos(item):
    logger.info("streamondemand-pureita.[leserietv findvideos]")
	
    itemlist = []

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title + "[COLOR orange]" + videoitem.title + "[/COLOR]"
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

# =================================================================


FilmFanart = "https://superrepo.org/static/images/fanart/original/script.artwork.downloader.jpg"
ThumbnailHome = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png"
thumbnail_novita="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"
thumbnail_lista="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"
thumbnail_categoria="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"
thumbnail_top="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"
thumbnail_cerca="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"
thumbnail_successivo="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"