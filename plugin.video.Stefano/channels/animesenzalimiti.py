# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA / XBMC Plugin
# Canale  animesenzalimiti
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import re
import xbmc

from core import logger
from core import servertools
from core import httptools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "animesenzalimiti"

host = "https://animeleggendari.com/"

def mainlist(item):
    logger.info("[streamondemand-pureita animesenzalimiti] mainlist")
    itemlist = [Item(channel=__channel__,
                     action="ultimiep",
                     title="[COLOR azure]Anime - [COLOR orange]Ultime Inserite[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_new_P.png"),
                Item(channel=__channel__,
                     action="cat_years",
                     title="[COLOR azure]Anime - [COLOR orange]Aggiornamenti per Data[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_new_P.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime - [COLOR orange]In Corso[/COLOR]",
                     url="%s/category/serie-anime-in-corso/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animation_P.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime - [COLOR orange]Complete[/COLOR]",
                     url="%s/category/serie-anime-concluse/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animation_P.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Anime - [COLOR orange]Categorie[/COLOR]",
                     url="%s/category/serie-anime-in-corso/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_genre_P.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime - [COLOR orange]Anime Leggendarie[/COLOR]",
                     url="%s/category/serie-anime-concluse/anime-leggendari/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR orange]Cerca ...[/COLOR]",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita animesenzalimiti] search")
    item.url = host + "/?s=" + texto
    try:
        return lista_anime(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# ==================================================================================================================================================

def categorie(item):
    logger.info("[streamondemand-pureita animesenzalimiti] categorie")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    #blocco = scrapertools.get_match(data, r'category menu-item-10950"><(.*?)</ul>')
    patron = r'<li id="menu-item-\d+" class[^>]+category menu-item-\d+"><a href="([^"]+)">([^<]+)<\/a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        if 'anime da vedere assolutamente' in scrapedtitle.lower(): continue
        itemlist.append(
                Item(channel=__channel__,
                     action="lista_anime",
                     title=scrapedtitle,
                     url=scrapedurl,
                     extra="tv",
                     thumbnail=item.thumbnail,
                     folder=True))

    return itemlist

# ==================================================================================================================================================

def cat_years(item):
    logger.info("[streamondemand-pureita animesenzalimiti] cat_years")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<option value="">Seleziona mese</option>(.*?)</select>')
    patron = r"<option value='(.*?)'>([^<]+)</option>"
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle=scrapedtitle.strip().capitalize()
        scrapedtitle="[COLOR yellow]" + scrapedtitle + "[/COLOR]"
        itemlist.append(
                Item(channel=__channel__,
                     action="lista_anime",
                     title=scrapedtitle,
                     url=scrapedurl,
                     extra="tv",
                     thumbnail=item.thumbnail,
                     folder=True))

    return itemlist
# ==============================================================================================================================================================================
'''
# ----------------------------------------------------------------------------------------------------------------
def animepopolari(item):
    logger.info("[streamondemand-pureita animesenzalimiti] mainlist")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r"<div class='widgets-grid-layout no-grav'>(.*?)</div>\s*</div>\s*</div>")
    patron = r'<a href="([^"]+)" title="([^"]+)"[^>]+>\s*<img.*?src="([^?]+)[^"]+"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        scrapedtitle = removestreaming(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodi",
                 contentType="tv",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="tv",
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))

    return itemlist
# ----------------------------------------------------------------------------------------------------------------
'''
# ==================================================================================================================================================

def ultimiep(item):
    logger.info("[streamondemand-pureita animesenzalimiti] ultimiep")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    blocco = scrapertools.get_match(data, r'Ultimi Anime Aggiunti</span>\s*</h4>(.*?)</li></ul>')
    patron = r'<a href="([^"]+)">\s*([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        if "SUB ITA" in scrapedtitle:
           lang=" ([COLOR yellow]Sub Ita[/COLOR])"
        else:
          if "ITA" in scrapedtitle:
           lang=" ([COLOR yellow]Ita[/COLOR])"

        scrapedtitle = scrapedtitle.replace("(Streaming &#038; Download)","").replace("/", "").replace("(Streaming e Download)", "").strip()
        scrapedtitle= scrapedtitle.replace("SUB ITA","").replace("ITA","").replace("&#8217;", "' ").replace("MOVIES","(Film)")

        scrapetitle=scrapedtitle.replace("Stagione", "").replace("Episodio", "")
        scrapetitle = re.sub(r"([0-9])", r"", scrapetitle).strip()

        scrapedthumbnail=""
        scrapedplot=""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodi",
                 contentType="episode",
                 title=scrapedtitle + lang,
                 fulltitle=scrapetitle,
                 show=scrapetitle,
                 url=scrapedurl,
                 extra="tv",
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo="tv"))

    patronvideos = r'<a class="next page-numbers" href="([^"]+)">&raquo;</a></div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_anime",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================

def lista_anime(item):
    logger.info("[streamondemand-pureita animesenzalimiti] lista_anime")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = r'<a class[^>]+\s*href="([^"]+)"\s*title="([^<]+)"><img[^>]+src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        if "SUB ITA" in scrapedtitle:
           lang=" ([COLOR yellow]Sub Ita[/COLOR])"
        if "ITA" in scrapedtitle:
           lang=" ([COLOR yellow]Ita[/COLOR])"
        else:
           lang=""

        scrapedtitle = scrapedtitle.replace("(Streaming &#038; Download)","").replace("/", "")
        scrapedtitle= scrapedtitle.replace("SUB ITA","").replace(" ITA","").replace("&#8217;", "' ")
        scrapedtitle = scrapedtitle.replace("MOVIES","(Film)")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        scrapedplot=""
		
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodi",
                 contentType="tv",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle  + lang,
                 url=scrapedurl,
                 extra="tv",
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo="tv"))

    patron = r'<a class="next page-numbers" href="([^"]+)">&raquo;</a></div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_anime",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================

def episodi(item):
    logger.info("[streamondemand-pureita animesenzalimiti] episodi")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.find_single_match(data, r'(?:<p style="text-align: left;">|<div class="pagination clearfix">\s*)(.*?)</span></a></div>')

    itemlist.append(
        Item(channel=__channel__,
             action="findvideos",
             contentType="tv",
             title="Episodio: 1",
             fulltitle=item.fulltitle + "- Ep. 1",
             url=item.url,
             extra="tv",
             thumbnail=item.thumbnail,
             plot="[COLOR orange]" + item.fulltitle + "[/COLOR]" + item.plot,
             folder=True))

    if blocco != "":
        patron = r'<a href="([^"]+)"><span class="pagelink">(\d+)</span></a>'
        matches = re.compile(patron, re.DOTALL).findall(data)
        for scrapedurl, scrapednumber in matches:
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="tv",
                     title="Episodio: %s" % scrapednumber,
                     fulltitle=item.fulltitle + "- Ep." + scrapednumber,
                     url=scrapedurl,
                     extra="tv",
                     thumbnail=item.thumbnail,
                     plot=item.plot,
                     folder=True))

    return itemlist

# ==================================================================================================================================================

def findvideos(item):
    logger.info("[streamondemand-pureita animesenzalimiti] findvideos")

    data = httptools.downloadpage(item.url).data
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        servername = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[COLOR azure]"+item.title, ' [[COLOR orange]'+servername.capitalize()+'[/COLOR]]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot=item.plot
        videoitem.channel = __channel__
    return itemlist





