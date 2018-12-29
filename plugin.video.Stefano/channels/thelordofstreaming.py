# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  TheLordOfStreaming
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import re
import urlparse
import base64

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "thelordofstreaming"
host = "http://www.thelordofstreaming.it"
headers = [['Referer', host]]



def mainlist(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/category/movie/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Wrestling[COLOR orange] - Novita'[/COLOR]",
                     action="peliculas",
                     url="%s/category/wrestling/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Novita[/COLOR]",
                     action="peliculas_tvshow",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Ultimi Episodi[/COLOR]",
                     action="peliculas_new",
                     url=host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Menu' ([COLOR azure]Archivio[/COLOR])",
                     action="mainlist_menu",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]


    return itemlist

# ==================================================================================================================================================

def mainlist_menu(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] mainlist_menu")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Lista[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serie-tv/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[COLOR orange] - Archivio[/COLOR]",
                     action="peliculas_list",
                     url="%s/serie-tv/" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist
	
# ==================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita TheLordOfStreaming] " + item.url + " search " + texto)
			
    try:
        if item.extra == "movie":
          item.url = host + "/?s=" + texto + "&submit=Cerca"
          return peliculas_srcmovie(item)
	  
        if item.extra == "serie":
          item.url = host + "/?s=" + texto + "+serie+tv&submit=Cerca"
          return peliculas_srctv(item)
		
		
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# ==================================================================================================================================================		
		
def peliculas(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<h1 class="entry-title"><a href="([^"]+)"\s*rel="bookmark">([^<]+)<\/a><\/h1>.*?'
    patron += '<img class=".*?"\s*src="([^"]+)" alt[^>]+[^A-Z]+(.*?)<\/'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = scrapertools.unescape(match.group(4))
        scrapedthumbnail = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        scrapedthumbnail = scrapedthumbnail.replace("-–-", "-%E2%80%93-")
        scrapedthumbnail = scrapedthumbnail.replace("’", "%E2%80%99")
        scrapedthumbnail = scrapedthumbnail.replace("à", "%C3%A0")
        scrapedtitle = scrapedtitle.replace("’", "").replace("&", "e")
        scrapedplot = scrapedplot.replace("/", "").replace("<em>", "")
        scrapedplot = scrapedplot.replace("<h1>", "").replace("<a>", "")
        scrapedplot = scrapedplot.replace("<p>", "").replace("a>", "")

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="meta-nav">&larr;</span> Articoli più vecchi</a></div>'
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

def peliculas_srcmovie(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas_srcmovie")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<h1 class="entry-title"><a href="([^"]+)" rel="bookmark">(.*?)</a></h1>.*?<p>(.*?)<'
    patron += '.*?rel="category tag">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle, scrapedplot, category in matches:
        if not "Movie" in category:
          continue

        scrapedthumbnail=""
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 fulltitle=title,
                 show=title,
                 folder=True), tipo="movie"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="meta-nav">&larr;</span> Articoli più vecchi</a></div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_srcmovie",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
	
# ==================================================================================================================================================

def peliculas_srctv(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas_srctv")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<h1 class="entry-title"><a href="([^"]+)" rel="bookmark">(.*?)</a></h1>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle in matches:
        if not "Serie TV" in scrapedtitle:
          continue
        if scrapedtitle=="Serie TV":
          continue
        scrapedplot=""
        scrapedthumbnail=""
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 fulltitle=title,
                 show=title,
                 folder=True), tipo="tv"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="meta-nav">&larr;</span> Articoli più vecchi</a></div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_srctv",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
# ==================================================================================================================================================

def peliculas_tvshow(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas_srctv")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<h1 class="entry-title"><a href[^>]+>([^1]+)[^>]+><\/h1>.*?'
    patron += '<div class="comments-link">.*?'
    patron += '<div class="entry-content">\s*[^>]+>.*?href="([^"]+)[^>]+><img class[^>]+src="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedtitle, scrapedurl, scrapedthumbnail  in matches:
        scrapedtitle=scrapedtitle.replace("&#038;", "").replace("&#82", "").strip()        
        if "attachment_id" in scrapedurl:
           scrapedurl= host+"/"+scrapedtitle.lower().replace(" ", "-")+"-serie-tv/"
		   
        scrapedtitle=scrapedtitle.replace("-", " ")
        scrapedplot=""

        title = scrapertools.decodeHtmlentities(scrapedtitle).strip()	

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 fulltitle=title,
                 show=title,
                 folder=True), tipo="tv"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="meta-nav">&larr;</span> Articoli più vecchi</a></div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tvshow",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def peliculas_new(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas_new")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<h1 class="entry-title"><a href="([^"]+)" rel="bookmark">([^1]+)([^<]+)</a></h1>\s*'
    patron += '<div class=".*?">\s*<.*?<time class[^>]+>(.*?)</time>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:

        scrapedate = scrapertools.unescape(match.group(4))
        scrapedep = scrapertools.unescape(match.group(3))
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        scrapedep = scrapedep.replace('SUBITA', 'SUB').replace("11;", "").replace("–", "-").strip()
        scrapedtitle=scrapedtitle.replace("&#038;", "").replace("&#82", "").strip()

        scrapedplot = ""
        scrapedthumbnail = ""
        if "Girada" in scrapedtitle or "WWE" in scrapedtitle:
		    continue
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos" if not "**" in scrapedep else "episodios_extra",
                 contentType="tv",
                 fulltitle=scrapedtitle.strip(),
                 show=scrapedtitle,
                 title="[COLOR azure]" +scrapedtitle + " - [COLOR aquamarine]"+ scrapedep + " - [COLOR yellow]" + scrapedate + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" ><span class="meta-nav">&larr;</span> Articoli più vecchi</a></div>'
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

# ==================================================================================================================================================

def peliculas_list(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas_list")
    itemlist = []	
    PERPAGE = 300
	
    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h1 class="entry-title">Serie TV</h1>(.*?)<h2 id="comments-title">')

    # Estrae i contenuti 
    patron = '<[^<]+href="([^>]+)">([^<]+)<\/a><\/li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)
    for i, (scrapedurl, scrapedtitle) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedtitle = scrapedtitle.replace("&#8211;", "-").strip()
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
                 title="[COLOR azure]" +title+ "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png",
                 fulltitle=title,
                 show=title,
                 folder=True))

    # Extrae el paginador
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_list",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist
# ==================================================================================================================================================

def peliculas_tv(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas_tv]")
    itemlist = []
    PERPAGE = 14
	
    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h1 class="entry-title">Serie TV</h1>(.*?)<h2 id="comments-title">')
    # Extrae las entradas
    patron = '<[^<]+href="([^>]+)">([^<]+)<\/a><\/li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for i, (scrapedurl, scrapedtitle ) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        scrapedtitle = scrapedtitle.replace("&#8211;", "-").strip()
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail=""
        scrapedplot=""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
                 contentType="tv",
                 title="[COLOR azure]" +title + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
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

def episodios_extra(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] peliculas_srctv")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<span style="text-decoration: underline;">([^<]+)<.*?(?:<span class="title-part"|)>([^<]+).*?<\/em>[^#]+[^>]+>([^<]+)<\/span><br \/>\s*(.*?)<\/a><\/'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedtitle, scrapedep, scraped_lang, scrapedurl in matches:
        #if scrapedep:
        scrapedtitle=scrapedtitle + " " + scrapedep
        scrapetitle=scrapedtitle
        scraped_lang=" ([COLOR yellow]" + scraped_lang + "[/COLOR])"

        scrapedplot=""
        scrapedthumbnail=""
        title = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos_tv",
                 title="[COLOR azure]" +title + "[/COLOR]" + scraped_lang,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 fulltitle=item.show + " - " + scrapedtitle, 
                 show=item.show + " - " + scrapedtitle,
                 plot="[COLOR orange][B]" + item.fulltitle + "[/B][/COLOR] " + item.plot,
                 folder=True))

    return itemlist

# ==================================================================================================================================================
	
def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '((?:.*?<a href="[^"]+"[^c]+class="external[^>]+>[^<]+</a>)+)'
        matches = re.compile(patron).findall(html)

        for data in matches:
            scrapedtitle = data.split('<a ')[0]

            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()

            if scrapedtitle != 'Film':
                scrapedtitle = scrapedtitle.replace('&#215;', ' X ')     
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos_tv" if not "cinemalibero" in data else "find_servers",
                         contentType="episode",
                         title="[COLOR azure]" + scrapedtitle + " ([COLOR yellow]" + lang_title + "[/COLOR])",
                         url=data if not "cinemalibero" in data else item.url,
                         thumbnail=item.thumbnail,
                         extra=scrapedtitle,
                         fulltitle=item.show + " - " + scrapedtitle + " (" + lang_title + ")",
                         plot="[COLOR orange][B]" + item.fulltitle + "[/B][/COLOR] " + item.plot,
                         show=item.show))

    logger.info("[streamondemand-pureita TheLordOfStreaming] episodios")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url).data
    data = scrapertools.decodeHtmlentities(data)

    lang_titles = []
    starts = []
    patron = r'Stagione'
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    for match in matches:
        season_title = match.group()
        if season_title != '':
            lang_titles.append('SUBITA' if 'SUB' in season_title.upper() else 'ITA')
            starts.append(match.end())

    i = 1
    len_lang_titles = len(lang_titles)

    while i <= len_lang_titles:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_lang_titles else -1

        html = data[inizio:fine]
        lang_title = lang_titles[i - 1]

        load_episodios(html, item, itemlist, lang_title)

        i += 1

    return itemlist

# ==================================================================================================================================================

# ==================================================================================================================================================
	
def findvideos_tv(item):
    logger.info("[streamondemand-pureita videotecaproject] findvideos")
    itemlist = []

    patron = '<a\s*href="([^"]+)"[^>]+>([^<]+)'
    matches = re.compile(patron, re.DOTALL).findall(item.url)

    for scrapedurl,scrapedtitle in matches:
        scrapedtitle=scrapedtitle.capitalize()
        if "Uplo" in scrapedtitle or "Altri" in scrapedtitle or "gator" in scrapedtitle \
            or "Nowdownload" in scrapedtitle or "Katfile" in scrapedtitle:
           continue
        if scrapedtitle=="–":
           continue
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 fulltitle=item.fulltitle,
                 show=item.fulltitle,
                 title="[[COLOR orange]" + scrapedtitle + "[/COLOR]] - [COLOR azure]" + item.fulltitle + "[/COLOR]",
                 url=scrapedurl.strip(),
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))

    return itemlist
# ==================================================================================================================================================
	
def find_servers(item):
    logger.info("[streamondemand-pureita TheLordOfStreaming] findvideos_server")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, "%s(.*?)<br />" % item.extra)

    # Extrae las entradas (carpetas)
    patron = '<a href="[^>]+goto\/([^"]+)" target="_blank" rel="nofollow" class="external">([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        url = scrapedurl.decode('base64')
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title="[[COLOR orange]" + scrapedtitle + "[/COLOR]] - [COLOR azure]" + item.fulltitle + "[/COLOR]",
                 url=url.strip(),
                 fulltitle=item.fulltitle,
                 show=item.show,
                 plot=item.plot,
                 thumbnail=item.thumbnail,
                 folder=True))

    return itemlist
	
	
# ==================================================================================================================================================

def play(item):
    itemlist=[]

    data = item.url

    if "rapidcrypt" in item.url:
       data = httptools.downloadpage(item.url).data
	  
    while 'vcrypt' in item.url:
        item.url = httptools.downloadpage(item.url, only_headers=True, follow_redirects=False).headers.get("location")
        data = item.url
		
    #logger.debug(data)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
	
# ==================================================================================================================================================
	
def findvideos(item):

    data = scrapertools.anti_cloudflare(item.url, headers)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        servername = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(['[[COLOR orange]' + servername.capitalize() + '[/COLOR]] - ', item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

# ==================================================================================================================================================
# ==================================================================================================================================================
# ==================================================================================================================================================
