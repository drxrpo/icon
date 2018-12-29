# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon
# ------------------------------------------------------------
# Stefano.- XBMC Plugin
# Canale documentaristreaming [Stefano]
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# by dentaku65, DrZ3r0
# ------------------------------------------------------------
import re
import urlparse

from core import httptools
from platformcode import logger
from core import scrapertools
from core.item import Item

__channel__ = "documentaristreaming"

host = "https://www.documentaristreaming.net/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Accept-Language', 'en-US,en;q=0.5'],
    ['Cache-Control', 'max-age=0'],
    ['Connection', 'keep-alive'],
    ['DNT', '1'],
    ['Referer', host],
    ['Upgrade-Insecure-Requests', '1']
]


def mainlist(item):
    logger.info("Stefano.documentaristreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Aggiornamenti[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url="%s/categorie-documentari-streaming/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist

def peliculas(item):
    logger.info("Stefano.documentaristreaming peliculas")
    itemlist = []

    # Download page
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data,
                                    '<h2>Recent Posts</h2>(.*?)<h2>')

    # Strip data
    patron = 'rel="bookmark">(.*?)<[^d]+div[^>]+>[^=]+="([^"]+)"[^<]+<img[^s]+src="(.*?)"'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapedtitle.strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    # Pages
    patronvideos = '<span class="current">[^<]+</span><a href="(.*?)"'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def peliculas_src(item):
    logger.info("Stefano.documentaristreaming peliculas")
    itemlist = []

    # Download page
    data = httptools.downloadpage(item.url, headers=headers).data

    # Strip data
    patron = '<div class="post-thumbnail">[^<]+<a href="([^"]+)"> <img width=[^s]+src="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapedurl
        scrapedtitle = scrapedtitle.replace(host, "")
        scrapedtitle = scrapedtitle.replace("/", "")
        scrapedtitle = scrapedtitle.replace("-", " ")
        scrapedtitle = scrapedtitle.title()
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    # Pages
    patronvideos = '<span class="current">[^<]+</span><a href="(.*?)"'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_src",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.Stefano)")


def categorias(item):
    logger.info("Stefano.documentaristreaming categorias")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    logger.info(data)

    # The categories are in the page  
    patron = '<a title=[^=]+="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for url, title in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(title)
        if scrapedtitle.startswith(("Categorie")):
            continue
        if scrapedtitle.startswith(("Forum")):
            continue
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_src",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=url,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[documentaristreaming.py] " + item.url + " search " + texto)
    item.url = host + "?s=" + texto
    try:
        return peliculas_src(item)

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
