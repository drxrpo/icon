# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita / XBMC Plugin
# Channel for linkstreaming
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# by H_2_0 for streamondemand-pureita & alfa-pureita*
# *Adjustment required for alfa-pureita
# ------------------------------------------------------------
import base64
import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod
from core import servertools

__channel__ = "linkstreaming"
host = "https://www.linkstreaming.tv"
headers = [['Referer', host]]

# ===================================================================================================================================================

def mainlist(item):
    logger.info("[streamondemand-pureita linkstreaming] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
             action="fichas",
             url=host + "/film/",
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Lista A/Z[/COLOR]",
             action="genere_az",
             url=host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
             action="genere",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Serie TV [COLOR orange]- Aggiornate[/COLOR]",
             action="fichas_tv",
             url=host + "/serie-tv-streaming/",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Serie TV [COLOR orange]- Ultimi Episodi[/COLOR]",
             action="fichas_new",
             url=host + '/ultimi-episodi/',
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
        Item(channel=__channel__,
             title="[COLOR orange]Cerca ...[/COLOR]",
             action="search",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ===================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita linkstreaming] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return fichas_search(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ===================================================================================================================================================

def genere_az(item):
    logger.info("[streamondemand-pureita linkstreaming] genere_az")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<ul class="AZList">(.+?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas_archive",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail='https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png',
                 folder=True))

    return itemlist

# ===================================================================================================================================================

def genere(item):
    logger.info("[streamondemand-pureita linkstreaming] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = 'Categorie</div> <ul>(.*?)</ul>\s*</div>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li class="cat-item cat-item-\d+"><a href="([^"]+)">(.*?)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas" if not "Serie Tv" in scrapedtitle else "fichas_tv",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail='https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png',
                 folder=True))

    return itemlist

# ===================================================================================================================================================

def fichas_archive(item):
    logger.info("[streamondemand-pureita linkstreaming] fichas_archive")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<img.*?src="([^"]+)" class="[^>]+"[^>]+>.*?' \
             '<td class="MvTbTtl">\s*<a href="([^"]+)"[^>]+>\s*' \
             '<strong>(.*?)<\/strong>.*?' \
             '<td>(.*?)<\/td>.*?' \
             '<a href="[^>]+rel="category">(.*?)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle, year, genre in matches:
        info_date='  [COLOR orange][' + year + " - " + genre + '][/COLOR]'
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if not "Serie Tv" in info_date else "episodios",
                 contentType="movie" if not "Serie Tv" in info_date else "tv",
                 title='[COLOR azure]' + scrapedtitle + '[/COLOR]' + info_date,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie' if not 'Serie Tv' in info_date else "tv"))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)">')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas_archive",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ===================================================================================================================================================

def fichas(item):
    logger.info("[streamondemand-pureita linkstreaming] fichas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a href="([^"]+)">\s*<div class="Image">[^>]+>.*?src="([^"]+)".*?>[^>]+>[^>]+>\s*' \
             '<h2 class="Title">([^<]+)<\/h2>.*?' \
             '<p>(.*?)<\/p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)">')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ===================================================================================================================================================

def fichas_tv(item):
    logger.info("[streamondemand-pureita linkstreaming] fichas_tv")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a href="([^"]+)">\s*<div class="Image">[^>]+><img.*?src="([^"]+)".*?' \
             '<h2 class="Title">([^<]+)</h2>.*?<p>(.*?)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 contentType="tv",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)">')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas_tv",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ===================================================================================================================================================

def fichas_new(item):
    logger.info("[streamondemand-pureita linkstreaming] fichas_new")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a href="([^"]+)">\s*<div class="Image">\s*' \
             '<figure class="[^>]+">\s*' \
             '<img.*?src="([^"]+)" alt="Image\s*([^\d+]+)([^<]+)">'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedep in matches:
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="tv",
                 title=scrapedtitle + scrapedep,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='tv'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)">')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas_new",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist



# ===================================================================================================================================================

def episodios(item):
    logger.info("[streamondemand-pureita linkstreaming] episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    #patron = '<a href="([^"]+)">\s*<div class="Image">\s*[^>]+>\s*' \
             #'<img.*?src="([^"]+)"\s*alt="Image\s*([^"]+)">'
    patron = '<td class[^>]+><a href="([^"]+)" class="MvTbImg">' \
             '<img src="([^"]+)" alt="Image\s*(.*?)"><\/a><\/td>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle   in matches:
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="tv",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=item.plot,
                 show=scrapedtitle), tipo='tv'))
				 
    patron = 'img.*?src=&quot[^h]+([^&]+).*?alt=&quot[^ ]+ ([^<]+)</span></a>' \
             '</td>\s*<td class="MvTbTtl"><a href="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedurl   in matches:
        scrapedtitle = scrapedtitle.replace("&quot;&gt;", "")
        scrapedtitle = scrapedtitle.replace("&amp;#8217;", "")
        scrapedtitle = scrapedtitle.replace("&amp;#8211;", "-")
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="tv",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=item.plot,
                 show=scrapedtitle), tipo='tv'))
				 
    return itemlist

# ===================================================================================================================================================

def fichas_search(item):
    logger.info("[streamondemand-pureita linkstreaming] fichas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<h1>Latest Movies</h1>(.*?)</section>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li class="[^>]+">\s*<article id[^>]+>.*?'
    patron += '<a href="([^"]+)">.*?'
    patron += '<h2 class="[^>]+">([^<]+)</h2>\s*<span class="Year">(.*?)</span>.*?'
    patron += '.*?<p>(.*?)</p>\s*'
    patron += '.*?[^>]+><span>Genere:[^>]+>\s*(.*?)\s*<'
	
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl,  scrapedtitle, year, scrapedplot, genre in matches:
        info_date='  [COLOR orange][' + year + " - " + genre + '][/COLOR]'
        scrapedthumbnail =""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if not "Serie" in genre else "episodios",
                 contentType="movie",
                 title='[COLOR azure]' + scrapedtitle + '[/COLOR]' + info_date,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 show=scrapedtitle), tipo='movie' if not "Serie" in genre else "tv"))


    return itemlist
# ===================================================================================================================================================

