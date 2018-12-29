# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale filmstream_biz
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

__channel__ = "filmstream_biz"
host = "https://streamfilm.club/"
headers = [['Referer', host]]


def mainlist(item):
    logger.info("[pureita filmstream_biz] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
             action="peliculas",
             url="%s/movies/" % host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Ultimi Inseriti[/COLOR]",
             action="peliculas_update",
             url=host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - 3D[/COLOR]",
             action="peliculas",
             url="%s/genre/3d/" % host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Richiesti[/COLOR]",
             action="top_richieste",
             url="%s/lista-film-richiesti-articolo-in-continuo-aggiorna" % host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
             action="genere",
             url="%s/movies/descendants-2/" % host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
        #Item(channel=__channel__,
             #title="[COLOR azure]Serie TV[/COLOR]",
             #action="peliculas_serie",
             #url="%s/tvshows/" % host,
             #extra="serie",
             #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
        Item(channel=__channel__,
             title="[COLOR orange]Cerca...[/COLOR]",
             action="search",
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ========================================================================================================================================================

def search(item, texto):
    logger.info("[pureita filmstream_biz] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return peliculas_search(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ========================================================================================================================================================		

def genere(item):
    logger.info("[pureita filmstream_biz] genere")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h2>Generi</h2>(.*?)</ul></nav>')

    # Extrae las entradas (carpetas)
    patron = '<li class=".*?"><a href="([^"]+)" >(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if "Action &amp; Adventure"  in scrapedtitle or "Sci-Fi &amp; Fantasy" in scrapedtitle:
	    continue
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ========================================================================================================================================================

def peliculas(item):
    logger.info("[pureita filmstream_biz] peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h1>.*?</h1>(.*?)Cerca il tuo film</h2>')	
	
    patron = '<div class="poster">\s*<img\s*src="([^"]+)"\s*alt="([^"]+)">\s*'
    patron += '<div class="rating"><span class=".*?"><\/span>\s*(.*?)<\/div>\s*'
    patron += '<div class="mepo">\s*<span class="quality">(.*?)<\/span>\s*<\/div>\s*<a href="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedthumbnail, scrapedtitle, rating, quality, scrapedurl in matches:
        if rating =="0" or rating =="10" or rating =="1":
          rating =""
        else:
          rating = " ([COLOR yellow]" + rating + "[/COLOR])"
        quality = " ([COLOR yellow]" + quality + "[/COLOR])"
        scrapedtitle = scrapedtitle.replace(" Streaming HD", "").replace("[HD]", "")
        scrapedtitle = scrapedtitle.replace(" Streaming", "")
        quality=quality.replace("PROSSIMAMENTE", "Pross.")

        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 show=scrapedtitle,
                 title=scrapedtitle + quality + rating,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)" ><span class="icon-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ========================================================================================================================================================

def peliculas_search(item):
    logger.info("[pureita filmstream_biz] peliculas_search")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*'
    patron += '<img src="([^"]+)"\s*alt="(.*?)" />'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle  in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)" ><span class="icon-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ========================================================================================================================================================

def peliculas_update(item):
    logger.info("[pureita filmstream_biz] peliculas_last")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<h2>Ultime uscite</h2>(.*?)<h2>Film</h2>')	
	
    patron = '<div class="poster">\s*<img\s*src="([^"]+)"\s*alt="([^"]+)">\s*'
    patron += '<div class="rating"><span class=".*?"></span>.*?</div>\s*'
    patron += '<div class=".*?">.*?</div><a href="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
        if "HD" in scrapedtitle:
          quality = " ([COLOR yellow]HD[/COLOR])"
        scrapedtitle = scrapedtitle.replace(" Streaming HD", "").replace("[HD]", "")
        scrapedtitle = scrapedtitle.replace(" Streaming", "").replace("HD", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle.strip() + quality,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)" ><span class="icon-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_update",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ========================================================================================================================================================

def top_richieste(item):
    logger.info("[pureita filmstream_biz] top_10")

    itemlist = []
	
    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
		
    patron = '<p><a href="([^"]+)".*?>([^<]+)</a></p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle  in matches:
        if "HD" in scrapedtitle:
          quality = " ([COLOR yellow]HD[/COLOR])"
        scrapedtitle=scrapedtitle.replace("HD", "").replace("Streaming", "").replace("[]", "")
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle=scrapedtitle.strip()
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle + quality,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))
				 
    return itemlist

# ========================================================================================================================================================


def top_10(item):
    logger.info("[pureita filmstream_biz] top_10")

    itemlist = []
	
    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
		
    patron = '<a href="([^"]+)"\s*class="tptn_link"><img src="([^"]+)" alt="[^>]+" title="([^<]+)" width[^>]+class=[^>]+>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle  in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))
				 
    return itemlist

# ========================================================================================================================================================

def peliculas_serie(item):
    logger.info("[pureita filmstream_biz] peliculas_last")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data	
	
    patron = '<div class="poster">\s*<img\s*src="([^"]+)"\s*alt="([^"]+)">\s*'
    patron += '<div class="rating"><span class=".*?"><\/span>.*?'
    patron += '<\/div>\s*[^>]+>\s*<\/div>\s*<a href="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv'))


    # Paginación
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)" ><span class="icon-chevron-right">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_serie",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ========================================================================================================================================================

def peliculas_new(item):
    logger.info("[pureita filmstream_biz] peliculas_new")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<div class="nav-menu"></div>(.*?)<br /></div>')
	
	
    patron = '<header class="entry-header no-anim" data-url="(.*?\/(.*?))\/">\s*<img width=".*?" height=".*?" src="([^<]+)" class[^>]+>'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if "serie-tv" in scrapedtitle:
		    continue
        scrapedtitle = scrapedtitle.replace("/", "")
        scrapedtitle = scrapedtitle.replace("filmstream.biz", "")
        scrapedtitle = scrapedtitle.replace("film-completo-online", "")
        scrapedtitle = scrapedtitle.replace("film-completi", "")
        scrapedtitle = scrapedtitle.replace("-streaming", "")
        scrapedtitle = scrapedtitle.replace("film-stream-biz", "")
        scrapedtitle = scrapedtitle.replace("film-altadefinizione", "")
        scrapedtitle = scrapedtitle.replace("alta-definizione", "")
        scrapedtitle = scrapedtitle.replace("online", "")
        scrapedtitle = scrapedtitle.replace("film", "")
        scrapedtitle = scrapedtitle.replace("gratis", "")
        scrapedtitle = scrapedtitle.replace("guarda-il", "")
        scrapedtitle = scrapedtitle.replace("stream", "")
        scrapedtitle = scrapedtitle.replace("netflix", "")
        scrapedtitle = scrapedtitle.replace("openload", "")
        scrapedtitle = scrapedtitle.replace("gratis-", "")
        scrapedtitle = scrapedtitle.replace("-hd", " [HD]")
        scrapedtitle = scrapedtitle.replace("-", " ")
        scrapedtitle = scrapedtitle.capitalize()



        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))


    return itemlist	

# ========================================================================================================================================================

def findvideos_tv(item):
    logger.info("pureita filmstream_biz findvideos")
    itemlist = []

    patron = '<a href="([^"]+)">(.*?)<\/a>'

    matches = re.compile(patron, re.DOTALL).findall(item.url)

    for scrapedurl, scrapedserver in matches:
        itemlist.append(
            Item(
                channel=__channel__,
                action="findvideos",
                fulltitle=item.scrapedtitle,
                show=item.scrapedtitle,
                title="[COLOR blue]" + item.title + "[/COLOR]" + " " + "[COLOR orange]" + scrapedserver + "[/COLOR]",
                url=scrapedurl,
                thumbnail=item.thumbnail,
                plot=item.plot,
                folder=True))

    return itemlist

# ========================================================================================================================================================
	
def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '((?:.*?<a href="[^"]+">[^<]+<\/a>)+)'
        matches = re.compile(patron).findall(html)

        for data in matches:
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle != 'Categorie':
                scrapedtitle = scrapedtitle.replace('&#215;', ' X ')
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos_tv",
                         contentType="episode",
                         title="[COLOR azure]%s[/COLOR]" % (scrapedtitle + " (" + lang_title + ")"),
                         url=data,
                         thumbnail=item.thumbnail,
                         plot=item.plot,
                         extra=item.extra,
                         fulltitle=scrapedtitle + " (" + lang_title + ")" + ' - ' + item.show,
                         show=item.show))

    logger.info("pureita filmstream_biz episodios")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url).data
    data = scrapertools.decodeHtmlentities(data)

    lang_titles = []
    starts = []
    patron = r"<u>Stagione .*?</u>"
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    for match in matches:
        season_title = match.group()
        if season_title != '':
            lang_titles.append('SUB ITA' if 'SUB' in season_title.upper() else 'ITA')
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

