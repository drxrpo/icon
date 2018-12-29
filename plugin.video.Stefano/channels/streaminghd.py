# -*-  coding: utf-8  -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  streaminghd
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

__channel__ = "streaminghd"
host = "https://streaminghd.fun/"
headers = [['Referer', host]]

def mainlist(item):
    logger.info("streamondemand-pureita streaminghd mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/film/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Aggiornati[/COLOR]",
                     action="peliculas_new",
                     url="%s/aggiornamenti-film/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Top IMDb[/COLOR]",
                     action="peliculas",
                     url="%s/piu-votati/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_sub_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Film [COLOR orange]- Novita'[/COLOR]",
                     #action="peliculas_update",
                     #url=host,
                     #extra="movie",
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     action="search",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV [COLOR orange]- Aggiornamenti[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serietv/aggiornamenti-serie-tv/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serietv/serie/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     url="%s/serietv/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================
	
def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h2>Genere</h2>(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
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

# ==============================================================================================================================================================================
	
def search(item, texto):
    logger.info("streamondemand-pureita streaminghd " + item.url + " search " + texto)
    
    try:
        if item.extra == "movie":
          item.url = host + "/?s=" + texto
          return peliculas_search(item)
	  
        if item.extra == "serie":
          item.url = host + "/serietv/?s=" + texto
          return peliculas_search(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================		
		
def peliculas(item):
    logger.info("streamondemand-pureita streaminghd peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)" alt="([^<]+)">\s*<div class="mepo"><span class="quality">\s*([^<]+) .*?'
    patron += '</div><div class="rating"><span class="icon-star2"></span>\s*(.*?)</div><a href="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url, match.group(5))
        votes = scrapertools.unescape(match.group(4))
        quality = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(1))
        votes=" [[COLOR yellow]" + votes + "[/COLOR]]"

        if "0" in votes:
         votes ="  [[COLOR yellow]" + "N/A" + "[/COLOR]]"
        quality ="  [[COLOR yellow]" + quality + "[/COLOR]]"
        if  "  [[COLOR yellow]" + " " + "[/COLOR]]" in quality:
         quality = ""
        scrapedtitle = scrapedtitle.replace("’", "'").replace(" &amp; ", " ").replace("&#8217;", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle + quality + votes,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)"><span class="icon-chevron-right">'
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

# ==============================================================================================================================================================================
		
def peliculas_new(item):
    logger.info("streamondemand-pureita streaminghd peliculas_new")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)">\s*<div class="mepo">\s*[^>]+>([^<]+)</span></div>\s*'
    patron += '<a href="([^"]+)"><div class="see"></div></a>\s*</div><div class[^>]+><h3><a href="[^"]+">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.unescape(match.group(4))
        scrapedurl = urlparse.urljoin(item.url, match.group(3))
        date = scrapertools.unescape(match.group(2))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(1))
        scrapedtitle = scrapedtitle.replace("’", "'").replace(" &amp; ", " ").replace("&#8217;", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle + "  [[COLOR yellow]" + date + "[/COLOR]]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)"><span class="icon-chevron-right">'
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

# ==============================================================================================================================================================================

def peliculas_update(item):
    logger.info("streamondemand-pureita streaminghd peliculas_update")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h2>Ultime Uscite</h2>(.*?)<h2>Films</h2>')	
	
    patron = '<img src="([^"]+)" alt="([^<]+)"><div class="rating"><span class="icon-star2">'
    patron += '</span>\s*([^<]+)</div><div class="featu">.*?</div><a href="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedthumbnail, scrapedtitle, votes, scrapedurl in matches:
        votes=" [[COLOR yellow]" + votes + "[/COLOR]]"
        if "0" in votes:
         votes ="  [[COLOR yellow]" + "N/A" + "[/COLOR]]"
        scrapedtitle = scrapedtitle.replace("’", "'").replace(" &amp; ", " ").replace("&#8217;", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle + votes,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo='movie'))


    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)" ><span class="icon-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_search(item):
    logger.info("streamondemand-pureita streaminghd peliculas_update")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h1>Risultati.*?</h1>(.*?)<div class="sidebar scrolling">')	
	
    patron = '<a href="([^"]+)"><img src="([^"]+)"\s*alt="([^<]+)"\s*/>'
    patron += '.*?"meta">[^>]+>\s*([^<]+)</span>.*?<div class="contenido"><p>(.*?)</p>'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedthumbnail, scrapedtitle, date, scrapedplot  in matches:
        scrapedtitle = scrapedtitle.replace("’", "'").replace(" &amp; ", " ").replace("&#8217;", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if item.extra == "movie" else "episodios",
                 contentType="movie" if item.extra == "movie" else "tv",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title='[COLOR azure]' + scrapedtitle + '[COLOR orange] [' + date + "][/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo="movie" if item.extra == "movie" else "tv"))

    return itemlist

# ==============================================================================================================================================================================	

def peliculas_tv(item):
    logger.info("streamondemand-pureita streaminghd peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)" alt="[^>]+">.*?<div class="rating"><span class="icon-star2">'
    patron += '</span>\s*([^<]+)</div>.*?[^>]+>.*?<a\s*href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.unescape(match.group(4))
        scrapedurl = urlparse.urljoin(item.url, match.group(3))
        votes = scrapertools.unescape(match.group(2))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(1))

        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        votes = votes.replace("[", "")
        votes = votes.replace("]", "")
        votes=" - [[COLOR yellow]" + votes + "[/COLOR]]"
        if "0" in votes:
         votes ="  [[COLOR yellow]" + "N/A" + "[/COLOR]]"
        scrapedtitle = scrapedtitle.replace("’", "'").replace(" &amp; ", " ").replace("&#8217;", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 contentType="serie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle + votes,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)"><span class="icon-chevron-right">'
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
				 
# ==============================================================================================================================================================================
	
def episodios(item):
    logger.info("streamondemand-pureita streaminghd episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<img src="([^"]+)"></a></div><div class="numerando">([^<]+)'
    patron += '</div><div class="episodiotitle"><a\s*href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedep, scrapedurl, scrapedtitle  in matches:
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedep + " " + scrapedtitle + "[/COLOR]",
                 contentType="episode",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=item.plot,
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

# ==============================================================================================================================================================================	
	
def findvideos(item):

    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.fulltitle, '[COLOR orange]' + videoitem.title + '[/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist



