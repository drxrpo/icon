# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale solostreaming_co
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import base64
import re
import urlparse

from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "solostreaming_co"
host = "https://www.solostreaming.co/"
headers = [['Referer', host]]



def mainlist(item):
    logger.info("pureita solostreaming_co mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film & Serie TV - [COLOR orange]Aggiornati[/COLOR]",
                     action="peliculas_update",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_new.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_new.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Per Genere[/COLOR]",
                     action="genere",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Film - [COLOR orange]Consigliati[/COLOR]",
                     #action="peliculas",
                     #url="%s/featured/" % host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),              
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/category/animazione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV - [COLOR orange]Novita'[/COLOR]",
                     action="peliculas_serie",
                     url="%s/category/serietv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Anime - [COLOR orange]Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/category/anime/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==================================================================================================================================================

def genere(item):
    logger.info("pureita solostreaming_co genere")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<h2 class="widgettitle">Genere</h2>(.*?)</select></form>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<option class=".*?" value=".*?">([^<]+)</option>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitle in matches:
        if "Anime " in scrapedtitle or "Serie Tv" in scrapedtitle or "Apocalittico" in scrapedtitle:
		   continue
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url="".join([host, "category/", scrapedtitle.lower()]),                 
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================

def peliculas(item):
    logger.info("pureita solostreaming_co peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="td-module-image">\s*<div class="td-module-thumb">'
    patron += '<a\s*href="([^"]+)"[^>]+><[^>]+src="(.*?)"[^>]+alt=".*?" title="([^"]+)"\s*/>.*?'
    patron += ' class="td-post-category">([^<]+)</'
    matches = re.compile(patron, re.DOTALL).findall(data)
	
    for scrapedurl, scrapedthumbnail, scrapedtitle, category   in matches:
        scrapedtitle = scrapedtitle.replace("Film", "").replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("&#038;", "e")
		
	if "SoloStreaming" in scrapedtitle: continue

		
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if "serie" in scrapedurl or "stagion" in scrapedurl or "Anime" in category else "findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv' if "serie" in scrapedurl or "stagion" in scrapedurl or "Anime" in category else "movie"))
				 
    next_page = scrapertools.find_single_match(data, '<link rel="next" href="([^"]+)" />')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================

def peliculas_update(item):
    logger.info("pureita solostreaming_co peliculas_update")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="td_module_16 td_module_wrap td-animation-stack">\s*'
    patron += '<div class="td-module-thumb"><a href="([^"]+)"[^>]+>[^>]+src="([^"]+)"[^>]+title="([^"]+)"\s*/>.*?'
    patron += ' class="td-post-category">([^<]+)</'
    matches = re.compile(patron, re.DOTALL).findall(data)
	
    for scrapedurl, scrapedthumbnail, scrapedtitle, category  in matches:
        scrapedtitle = scrapedtitle.replace("Film", "").replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("&#038;", "e")
	
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

    

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if "serie" in scrapedurl or "stagion" in scrapedurl or "Anime" in category else "findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv' if "serie" in scrapedurl or "stagion" in scrapedurl or "Anime" in category else "movie"))

    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"><i class="td-icon-menu-right"></i>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================

def peliculas_serie(item):
    logger.info("pureita solostreaming_co peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a\s*href="([^"]+)"[^>]+title="([^"]+)"><img[^>]+src="([^"]+)" alt[^>]+/>'
    matches = re.compile(patron, re.DOTALL).findall(data)
	
    for scrapedurl, scrapedtitle, scrapedthumbnail  in matches:
        scrapedtitle = scrapedtitle.replace("&#038;", "e").replace("Streaming", "")

		
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if "serie" in scrapedurl or "stagion" in scrapedurl or "Anime" in scrapedtitle else "findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv' if "serie" in scrapedurl or "stagion" in scrapedurl or "Anime" in scrapedtitle else "movie"))
				 
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"><i class="td-icon-menu-right"></i>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================
	
def episodios(item):
    logger.info("pureita solostreaming_co episodios")

    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a\s*href="([^"]+)">(.*?)<\/.*?strong>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        if "Fonte" in scrapedtitle or "Forum" in scrapedtitle or "i class" in scrapedtitle:
		    continue
        scrapedtitle = scrapedtitle.replace("/", "")
        scrapedtitle = scrapedtitle.replace(">", "")
        scrapedtitle = scrapedtitle.replace("strong", "")
        scrapedtitle = scrapedtitle.replace("<a", "")
        scrapedtitle = scrapedtitle.replace("<", "")
        scrapedtitle = scrapedtitle.replace("Cassetta", "")
        scrapedtitle = scrapedtitle.replace("span style=", "")
        scrapedtitle = scrapedtitle.replace("color:", "")
        scrapedtitle = scrapedtitle.replace("#ff0000;", "")
        scrapedtitle = scrapedtitle.replace('"', "")			
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))
				 
    patron = '<a href="([^"]+)"\s*target[^>]+>.*?([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        if "Fonte" in scrapedtitle or "Forum" in scrapedtitle or "br />" in scrapedtitle: 
		    continue
        scrapedtitle = scrapedtitle.replace("/", "")
        scrapedtitle = scrapedtitle.replace(">", "")
        scrapedtitle = scrapedtitle.replace("strong", "")
        scrapedtitle = scrapedtitle.replace("<a", "")
        scrapedtitle = scrapedtitle.replace("<", "")
        scrapedtitle = scrapedtitle.replace("Cassetta", "")
        scrapedtitle = scrapedtitle.replace("span style=", "")
        scrapedtitle = scrapedtitle.replace("color:", "")
        scrapedtitle = scrapedtitle.replace("#ff0000;", "")
        scrapedtitle = scrapedtitle.replace('"', "")			
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))

    return itemlist
	
# ==================================================================================================================================================

def search(item, texto):
    logger.info("[pureita solostreaming_co] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return peliculas_update(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==================================================================================================================================================
	
def findvideos(item):

    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.title = "".join(['[[COLOR orange]' + server + '[/COLOR]] - ', item.fulltitle])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

# ==================================================================================================================================================


